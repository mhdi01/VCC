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
            raise HTTPException(status_code=400, detail="Schedule SeatLimit exceed the Capacity Limit in the specific time range")
        return True


def check_book_constraints(db, capacity, schedule, update_data=None):
    if not check_type_constraints(db, schedule, capacity, update_data):
        return False
    
    if update_data and 'StartTime' in update_data: schedule_start_time = time.mktime(update_data['StartTime'].timetuple())
    elif update_data and 'StartTime' not in update_data: schedule_start_time = schedule.StartTime
    else: schedule_start_time = time.mktime(schedule.StartTime.timetuple())

    if update_data and 'EndTime' in update_data: schedule_end_time = time.mktime(update_data['EndTime'].timetuple())
    elif update_data and 'Endtime' not in update_data: schedule_end_time = schedule.EndTime
    else: schedule_end_time = time.mktime(schedule.EndTime.timetuple())

    sch_limit = ''
    if update_data and 'SeatLimit' in update_data: sch_limit = update_data['SeatLimit']
    else: sch_limit = schedule.SeatLimit

    problem = Problem()
    conflicting_schedules = db.query(Schedule.id)\
        .filter(
            Schedule.CapacityId == capacity.id,
            Schedule.EndTime >= schedule_start_time,
            Schedule.StartTime <= schedule_end_time
        ).all()
    schedule_vars = [
        f"{obj.id}"
        for obj in conflicting_schedules
    ]

    # Add variables for new schedule within its time range
    new_schedule_var = f"NewSchedule"
    problem.addVariable(new_schedule_var, range(sch_limit + 1))


    # Add variables for existing schedules within the time range
    for schedule_var in schedule_vars:
        schedule_limit = db.query(Schedule).filter(Schedule.id == schedule_var).first().SeatLimit
        problem.addVariable(schedule_var, range(schedule_limit + 1))


    # Capacity limit constraint for existing schedules
    for schedule_var in schedule_vars:
        schedule_limit = db.query(Schedule).filter(Schedule.id == schedule_var).first().SeatLimit
        problem.addConstraint(lambda schedule, limit=schedule_limit: schedule <= limit, (schedule_var,))


    problem.addConstraint(lambda *schedules, total_limit=capacity.CapacityLimit: sum(schedules) <= total_limit, [new_schedule_var] + schedule_vars)

    solution = problem.getSolution()
    if solution['NewSchedule'] != sch_limit:
        print('Is Not Optimal')
        return False
    
    else:
        print('IsOptimal')
        return True
