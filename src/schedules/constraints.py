import models
from sqlalchemy.sql import func
import time
from models import *
from fastapi import HTTPException
from cpmpy import *
from cpmpy.solvers import CPM_ortools
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

    if update_data and 'StartTime' in update_data:
        schedule_start_time = time.mktime(update_data['StartTime'].timetuple())
    elif update_data and 'StartTime' not in update_data:
        schedule_start_time = schedule.StartTime
    else:
        schedule_start_time = time.mktime(schedule.StartTime.timetuple())

    if update_data and 'EndTime' in update_data:
        schedule_end_time = time.mktime(update_data['EndTime'].timetuple())
    elif update_data and 'EndTime' not in update_data:
        schedule_end_time = schedule.EndTime
    else:
        schedule_end_time = time.mktime(schedule.EndTime.timetuple())

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
            Schedule.CapacityId == capacity.id,
            Schedule.EndTime >= schedule_start_time,
            Schedule.StartTime <= schedule_end_time
        ).all()
    

    # Create variables for existing schedules within the time range
    schedule_vars = [intvar(0, s.SeatLimit, name=f"Schedule_{s}") for s in conflicting_schedules]


    # Total seat limit constraint for existing and new schedules
    total_limit = capacity.CapacityLimit
    sch_sum = sum(obj.ub for obj in schedule_vars)
    model += sch_sum + new_schedule_var <= total_limit
    
    assert sum(schedule_vars) + new_schedule_var <= total_limit, "Capacity Limit exceed the Cluster Limit in the specific time range"
    # Find the optimal solution to maximize the new schedule's seat limit (if needed)
    model.maximize(new_schedule_var)

    # Use the solver to find the optimal solution
    solver = CPM_ortools(model)
    solution = solver.solve()

    if not solution:
        print('No feasible solution')
        return False

    if new_schedule_var.value() != sch_limit:
        print('Is Not Optimal')
        return False
    else:
        print('Is Optimal')
        return True
