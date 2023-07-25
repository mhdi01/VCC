import models
from sqlalchemy.sql import func
import time
from sqlalchemy.orm import Session
from sqlalchemy import and_ , or_
from models import *
from fastapi import HTTPException
from . import schemas
from constraint import Problem, AllDifferentConstraint

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


def check_book_constraints(db, cluster, capacity, update_data=None):
    if not check_type_constraints(db, cluster, capacity, update_data):
        return False
    
    if update_data and 'StartTime' in update_data: capacity_start_time = time.mktime(update_data['StartTime'].timetuple())
    elif update_data and 'StartTime' not in update_data: capacity_start_time = capacity.StartTime
    else: capacity_start_time = time.mktime(capacity.StartTime.timetuple())

    if update_data and 'EndTime' in update_data: capacity_end_time = time.mktime(update_data['EndTime'].timetuple())
    elif update_data and 'Endtime' not in update_data: capacity_end_time = capacity.EndTime
    else: capacity_end_time = time.mktime(capacity.EndTime.timetuple())

    if update_data and 'CapacityLimit' in update_data: cap_limit = update_data['CapacityLimit']
    else: cap_limit = capacity.CapacityLimit

    problem = Problem()
    conflicting_capacities = db.query(
        Capacity
        ).filter(
        Capacity.ClusterId == cluster.id
        ).filter(
        and_(Capacity.EndTime >= capacity_start_time, Capacity.StartTime <= capacity_end_time)
        ).all()

    capacity_vars = [
        f"{obj.id}"
        for obj in conflicting_capacities
    ]

    # Add variables for new capacity within its time range
    new_capacity_var = f"NewCapacity"
    problem.addVariable(new_capacity_var, range(cap_limit + 1))


    # Add variables for existing capacities within the time range
    for capacity_var in capacity_vars:
        capacity_limit = db.query(Capacity).filter(Capacity.id == capacity_var).first().CapacityLimit
        problem.addVariable(capacity_var, range(capacity_limit + 1))


    # Capacity limit constraint for existing capacities
    for capacity_var in capacity_vars:
        capacity_limit = db.query(Capacity).filter(Capacity.id == capacity_var).first().CapacityLimit
        problem.addConstraint(lambda capacity, limit=capacity_limit: capacity <= limit, (capacity_var,))


    problem.addConstraint(lambda *capacities, total_limit=cluster.MaxLimit: sum(capacities) <= total_limit, [new_capacity_var] + capacity_vars)

    solution = problem.getSolution()
    if solution['NewCapacity'] != cap_limit:
        print('Is Not Optimal')
        raise HTTPException(status_code=400, detail="Capacity Limit exceed the Cluster Limit in the specific time range")
    
    else:
        print('IsOptimal')
        return True
