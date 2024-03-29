import models
from sqlalchemy.sql import func
import time
from sqlalchemy import and_ , or_
from models import *
from actions import solve_maintenance_conflict
from fastapi import HTTPException
from cpmpy import *
from cpmpy.solvers import CPM_ortools
from sqlalchemy import and_, or_


import time

def check_type_constraints(db, cluster, capacity, update_data=None):
    if update_data and 'SeatType' in update_data: seat_type = update_data['SeatType']
    else: seat_type = capacity.SeatType.value
    if cluster.SeatType.value!= seat_type:
        print("SeatTypes are Not the same Capacity SeatType is {0} , Cluster SeatType is {1}".format(capacity.SeatType.value, seat_type))
        raise HTTPException(status_code=400, detail="SeatType is not as same as the cluster seatType")

    return True
    

def check_update_constraint(capacity, data):
    if 'SeatType' in data:
        if capacity.CapacityCluster.SeatType != data['SeatType']:
            print("SeatTypes are Not the same Capacity SeatType is {0} , Cluster SeatType is {1}".format(data['SeatType'], capacity.CapacityCluster.SeatType))
            raise HTTPException(status_code=400, detail="SeatType is not as same as the cluster seatType")
        return True


def check_book_constraints(db, cluster, capacity, update_data=None, from_schedule=None):
    if not check_type_constraints(db, cluster, capacity, update_data):
        return False
    
    if update_data and 'StartTime' in update_data: capacity_start_time = time.mktime(update_data['StartTime'].timetuple())
    elif update_data and 'StartTime' not in update_data: capacity_start_time = capacity.StartTime
    else:
        if from_schedule:
            capacity_start_time = capacity.StartTime
        else:
            capacity_start_time = time.mktime(capacity.StartTime.timetuple())

    if update_data and 'EndTime' in update_data: capacity_end_time = time.mktime(update_data['EndTime'].timetuple()) + 120
    elif update_data and 'Endtime' not in update_data: capacity_end_time = capacity.EndTime + 120
    else:
        if from_schedule:
            capacity_end_time = capacity.EndTime + 120
        else: 
            capacity_end_time = time.mktime(capacity.EndTime.timetuple()) + 120

    if update_data and 'CapacityLimit' in update_data: cap_limit = update_data['CapacityLimit']
    else: cap_limit = capacity.CapacityLimit

    model = Model()

    if not solve_maintenance_conflict(capacity_start_time, capacity_end_time, cluster.MaintenanceStartTime, cluster.MaintenanceEndTime):
        raise HTTPException(status_code=400, detail="Capacity Time range is in Maintenance Time range")
    
    # Create variables for the new schedule within its time range
    new_capacity_var = intvar(0, cap_limit, name="NewCapacity")

    conflicting_capacities = db.query(
        Capacity.id, Capacity.CapacityLimit
        ).filter(
        Capacity.ClusterId == cluster.id,
        Capacity.EndTime >= capacity_start_time,
        Capacity.StartTime <= capacity_end_time,
        Capacity.PlanType == models.PlanTypeEnum.Fixed
        ).all()
    
    # Create variables for existing capacities within the time range
    capacity_vars = [intvar(0, s.CapacityLimit, name=f"Capacity_{s}") for s in conflicting_capacities]

    # Total seat limit constraint for existing and new schedules
    total_limit = cluster.MaxLimit
    cap_sum = sum(obj.ub for obj in capacity_vars)
    if update_data or from_schedule:
        cap_sum = cap_sum - capacity.CapacityLimit

    if cap_sum <= 0 : cap_sum = cap_sum * -1
    model += cap_sum + new_capacity_var <= total_limit
    

    assert cap_sum + new_capacity_var <= total_limit, "Capacity Limit exceed the Cluster Limit in the specific time range"
    # Find the optimal solution to maximize the new schedule's seat limit (if needed)
    model.maximize(new_capacity_var)


    # Use the solver to find the optimal solution
    solver = CPM_ortools(model)
    solution = solver.solve()

    if not solution:
        raise HTTPException(status_code=400, detail="Capacities CapacityLimit exceed the Cluster MaxLimit")

    if new_capacity_var.value() != cap_limit:
        raise HTTPException(status_code=400, detail="Capacities CapacityLimit exceed the Cluster MaxLimit")
    
    else:
        print('Is Optimal')
        return True

