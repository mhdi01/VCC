import models
from sqlalchemy.sql import func
import time
from models import *
from fastapi import HTTPException
from cpmpy import *
from cpmpy.solvers import CPM_ortools
from actions import solve_maintenance_conflict
import time
from sqlalchemy import and_, or_

def check_type_constraints(db, schedule, capacity, update_data=None):
    if update_data and 'SeatType' in update_data: seat_type = update_data['SeatType']
    else: seat_type = schedule.SeatType.value
    if capacity.SeatType.value != seat_type:
        print("SeatTypes are Not the same Schedule SeatType is {0} , Capacity SeatType is {1}".format(seat_type, capacity.SeatType.value))
        raise HTTPException(status_code=400, detail="SeatType is not as same as the capacity seatType")

    return True
    

def check_update_constraint(schedule, data):
    if 'SeatType' in data:
        if schedule.ScheduleCapacity.SeatType.value != data['SeatType']:
            print("SeatTypes are Not the same Schedule SeatType is {0} , Capacity SeatType is {1}".format(data['SeatType'], schedule.ScheduleCapacity.SeatType.value))
            raise HTTPException(status_code=400, detail="SeatType is not as same as the capacity seatType")
        return True



def check_book_constraints(db, capacity, schedule, update_data=None):
    if not check_type_constraints(db, schedule, capacity, update_data):
        return False

    if update_data and 'StartTime' in update_data:
        schedule_start_time = time.mktime(update_data['StartTime'].timetuple())
    elif update_data and 'StartTime' not in update_data:
        schedule_start_time = schedule.StartTime
    else:
        schedule_start_time = time.mktime(schedule.StartTime.timetuple())

    if update_data and 'EndTime' in update_data:
        schedule_end_time = time.mktime(update_data['EndTime'].timetuple()) + 120
    elif update_data and 'EndTime' not in update_data:
        schedule_end_time = schedule.EndTime + 120
    else:
        schedule_end_time = time.mktime(schedule.EndTime.timetuple()) + 120

    if update_data and 'SeatLimit' in update_data:
        sch_limit = update_data['SeatLimit']
    else:
        sch_limit = schedule.SeatLimit

    # Define the constraint satisfaction problem (CSP) using cpmpy
    model = Model()

    # Create variables for the new schedule within its time range
    new_schedule_var = intvar(0, sch_limit, name="NewSchedule")

    if not solve_maintenance_conflict(schedule_start_time, schedule_end_time, capacity.CapacityCluster.MaintenanceStartTime, capacity.CapacityCluster.MaintenanceEndTime):
        raise HTTPException(status_code=400, detail="Schedule Time range is in Maintenance Time range")

    if not check_schedule_time_period(schedule_start_time, schedule_end_time, capacity.StartTime, capacity.EndTime):
        raise HTTPException(status_code=400, detail="Schedule Time range is not in capacity Time range")
    
    conflicting_schedules = db.query(Schedule.id, Schedule.SeatLimit)\
        .filter(
            Schedule.CapacityId == capacity.id,
            Schedule.EndTime >= schedule_start_time,
            Schedule.StartTime <= schedule_end_time
        ).all()
    

    # Create variables for existing schedules within the time range
    schedule_vars = [intvar(0, s.SeatLimit, name=f"Schedule_{s}") for s in conflicting_schedules]


    # Total seat limit constraint for existing and new schedules
    total_limit = capacity.CapacityLimit
    sch_sum = sum(obj.ub for obj in schedule_vars)
    if update_data:
        sch_sum = sch_sum - schedule.SeatLimit
    
    if sch_sum <= 0 : sch_sum = sch_sum * -1
    model += int(sch_sum) + new_schedule_var <= total_limit
    
    assert sum(schedule_vars) + new_schedule_var <= total_limit, "Capacity Limit exceed the Cluster Limit in the specific time range"
    # Find the optimal solution to maximize the new schedule's seat limit (if needed)
    model.maximize(new_schedule_var)

    # Use the solver to find the optimal solution
    solver = CPM_ortools(model)
    solution = solver.solve()

    if not solution:
        raise HTTPException(status_code=400, detail="Schedule SeatLimit exceed the Capacity Limit in the specific time range")

    if new_schedule_var.value() != sch_limit:
        raise HTTPException(status_code=400, detail="Schedule SeatLimit exceed the Capacity Limit in the specific time range")
    
    else:
        print('Is Optimal')
        return True



def check_book_cluster_constraints(db, schedule, cluster, update_data=None):
    if update_data and 'StartTime' in update_data:
        schedule_start_time = time.mktime(update_data['StartTime'].timetuple())
    elif update_data and 'StartTime' not in update_data:
        schedule_start_time = schedule.StartTime
    else:
        schedule_start_time = time.mktime(schedule.StartTime.timetuple())

    if update_data and 'EndTime' in update_data:
        schedule_end_time = time.mktime(update_data['EndTime'].timetuple()) + 120
    elif update_data and 'EndTime' not in update_data:
        schedule_end_time = schedule.EndTime + 120
    else:
        schedule_end_time = time.mktime(schedule.EndTime.timetuple()) + 120

    if update_data and 'SeatLimit' in update_data:
        sch_limit = update_data['SeatLimit']
    else:
        sch_limit = schedule.SeatLimit

    # Define the constraint satisfaction problem (CSP) using cpmpy
    model = Model()

    # Create variables for the new schedule within its time range
    new_schedule_var = intvar(0, sch_limit, name="NewSchedule")

    conflicting_schedules = db.query(Schedule.id, Schedule.SeatLimit)\
        .filter(
            Schedule.ClusterId == cluster.id,
            Schedule.EndTime >= schedule_start_time,
            Schedule.StartTime <= schedule_end_time
        ).all()
    

    # Create variables for existing schedules within the time range
    schedule_vars = [intvar(0, s.SeatLimit, name=f"Schedule_{s}") for s in conflicting_schedules]


    # Total seat limit constraint for existing and new schedules
    total_limit = cluster.MaxLimit
    sch_sum = sum(obj.ub for obj in schedule_vars)
    if update_data:
        sch_sum = sch_sum - schedule.SeatLimit
    
    if sch_sum <= 0 : sch_sum = sch_sum * -1
    model += int(sch_sum) + new_schedule_var <= total_limit
    
    assert sum(schedule_vars) + new_schedule_var <= total_limit, "Capacity Limit exceed the Cluster Limit in the specific time range"
    # Find the optimal solution to maximize the new schedule's seat limit (if needed)
    model.maximize(new_schedule_var)

    # Use the solver to find the optimal solution
    solver = CPM_ortools(model)
    solution = solver.solve()

    if not solution:
        raise HTTPException(status_code=400, detail="Schedule SeatLimit exceed the Cluster Limit in the specific time range")

    if new_schedule_var.value() != sch_limit:
        raise HTTPException(status_code=400, detail="Schedule SeatLimit exceed the Cluster Limit in the specific time range")
    
    else:
        print('Is Optimal')
        return True



def check_schedule_time_period(start_time, end_time, capacity_start_time, capacity_end_time):
    # Check for overlaps using cpmpy
    overlap_model = Model()

    # Variables to represent the start and end times of the new schedule
    schedule_start_var = IntVar(0, int(start_time))
    schedule_end_var = IntVar(0, int(end_time))

    # Constraint: schedule_end_var should be greater than or equal to schedule_start_var
    overlap_model += schedule_end_var >= schedule_start_var

    # Constraint: new schedule should not overlap with capacity time period
    overlap_model += (schedule_start_var.ub >= int(capacity_start_time)) and (schedule_end_var.ub <= int(capacity_end_time))

    # Check if the model is satisfiable (i.e., no overlap exists)
    if overlap_model.solve():
        return True
    else:
        return False
