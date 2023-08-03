from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, FastAPI, HTTPException, APIRouter

import models
from . import schemas, constraints
from actions import id_generator, TableRepository
from clusters import crud as crudcluster
from capacities import crud as capacitycrud
import time
import datetime



def get_schedules(profile_id: str, capacity_id: str, db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Schedule).filter(models.Schedule.ProfileId == profile_id).filter(models.Schedule.CapacityId == capacity_id).offset(skip).limit(limit).all()


def book_schedule(db: Session, schedule: schemas.Schedule, capacity_id: str, profile_id: str):
    capacity = db.query(models.Capacity).filter(models.Capacity.id == capacity_id).first()
    if not capacity:
        raise HTTPException(status_code=400, detail="Unable to Create the Schedule")

    if capacity.PlanType != models.PlanTypeEnum.Volume:
        raise HTTPException(status_code=400, detail="PlanType Should Be Volume to reserve a schedule")
    
    if not constraints.check_book_constraints(db, capacity, schedule):
        raise HTTPException(status_code=400, detail="Constraints are not passed")

    cluster = crudcluster.retrieve_cluster(cluster_id=capacity.ClusterId, db=db)
    if not constraints.check_book_cluster_constraints(db, schedule, cluster):
        raise HTTPException(status_code=400, detail="Constraints are not passed")
    
    try:
        schedule.ProfileId = profile_id
        schedule.CapacityId = capacity_id
        schedule.StartTime = time.mktime(schedule.StartTime.timetuple())
        schedule.EndTime = time.mktime(schedule.EndTime.timetuple())
        schedule.id = id_generator()
        db_schedule = models.Schedule(**schedule.model_dump())
        db.add(db_schedule)
        db.commit()
        db.refresh(db_schedule)

    except Exception as e:
        print("Error creating Schedule",e.__str__())
        raise HTTPException(status_code=400, detail="Unable to Create the Schedule")
    
    return db_schedule


def retrieve_schedule(profile_id:str, capacity_id: str, schedule_id: str, db:Session):
    return db.query(models.Schedule).filter(models.Schedule.id == schedule_id).filter(models.Schedule.ProfileId == profile_id).filter(models.Schedule.CapacityId == capacity_id).first()


def update_schedule(profile_id:str, capacity_id: str, schedule_id: str, data: schemas.ScheduleBase, db:Session):
    repo = TableRepository(db, models.Schedule)
    schedule = repo.find_by_id(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail='Schedule Not found')
    capacity = db.query(models.Capacity).filter(models.Capacity.id == capacity_id).first()
    if not capacity:
        raise HTTPException(status_code=400, detail="Unable to Update the Schedule")

    if capacity.PlanType != models.PlanTypeEnum.Volume:
        raise HTTPException(status_code=400, detail="PlanType Should Be Volume to reserve a schedule")
    
    update_data = data.model_dump(exclude_unset=True)
    if schedule:
        if not constraints.check_book_constraints(db, capacity, schedule, update_data):
            raise HTTPException(status_code=400, detail="Constraints are not passed")
        
        cluster = capacity.CapacityCluster
        if not constraints.check_book_cluster_constraints(db, schedule, cluster, update_data):
            raise HTTPException(status_code=400, detail="Constraints are not passed")


        if 'StartTime' in update_data:
            update_data['StartTime'] = time.mktime(update_data['StartTime'].timetuple())
        if 'EndTime' in update_data:
            update_data['EndTime'] = time.mktime(update_data['EndTime'].timetuple())

        update_data['ProfileId'] = profile_id
        update_data['CapacityId'] = capacity_id

        try:
            repo.set_attrs(schedule, update_data)
            db.commit()
            db.refresh(schedule)

        except Exception as e:
            print("Error Updating Schedule",e.__str__())
            raise HTTPException(status_code=400, detail="Unable to Update the Schedule")
            
    return schedule


def delete_schedule(profile_id:str, capacity_id: str, schedule_id: str, db:Session):
    obj = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).filter(models.Schedule.ProfileId == profile_id).filter(models.Schedule.CapacityId == capacity_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return

