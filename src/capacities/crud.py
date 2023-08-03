from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, FastAPI, HTTPException, APIRouter

import models
from . import schemas, constraints
from actions import id_generator, TableRepository
import time
import datetime



def get_capacities(profile_id: str, db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Capacity).filter(models.Capacity.ProfileId == profile_id).offset(skip).limit(limit).all()


def create_capacity(db: Session, capacity: schemas.Capacity, profile_id: str):
    cluster = db.query(models.Cluster).filter(models.Cluster.id == capacity.ClusterId).first()
    if not cluster:
        raise HTTPException(status_code=400, detail="Cluster Doesnt Exists")

    if capacity.PlanType == models.PlanTypeEnum.Fixed.value:
        if not constraints.check_book_constraints(db, cluster, capacity):
            raise HTTPException(status_code=400, detail="Constraints are not passed")


    try:
        capacity.ProfileId = profile_id
        capacity.StartTime = time.mktime(capacity.StartTime.timetuple())
        capacity.EndTime = time.mktime(capacity.EndTime.timetuple())
        capacity.id = id_generator()
        db_capacity = models.Capacity(**capacity.model_dump())
        db.add(db_capacity)
        db.commit()
        db.refresh(db_capacity)
    except Exception as e:
        print("Error creating Cluster",e.__str__())
        raise HTTPException(status_code=400, detail="Unable to Create the Capacity")
    
    return db_capacity


def retrieve_capacity(profile_id:str, capacity_id: str, db:Session):
    return db.query(models.Capacity).filter(models.Capacity.id == capacity_id).filter(models.Capacity.ProfileId == profile_id).first()


def update_capacity(profile_id:str, capacity_id: str, data: schemas.CapacityBase, db:Session):
    repo = TableRepository(db, models.Capacity)
    capacity = repo.find_by_id(capacity_id)
    if not capacity:
        raise HTTPException(status_code=404, detail='Capacity Not found')
    update_data = data.model_dump(exclude_unset=True)
    if capacity:
        if 'PlanType' in update_data and update_data['PlanType'] == models.PlanTypeEnum.Fixed.value:
            if not constraints.check_book_constraints(db, capacity.CapacityCluster, capacity, update_data):
                raise HTTPException(status_code=400, detail="Constraints are not passed")
            
        if 'StartTime' in update_data:
            update_data['StartTime'] = time.mktime(update_data['StartTime'].timetuple())

        if 'EndTime' in update_data:
            update_data['EndTime'] = time.mktime(update_data['EndTime'].timetuple())

        update_data['ProfileId'] = profile_id
        try:
            repo.set_attrs(capacity, update_data)
            db.commit()
            db.refresh(capacity)

        except Exception as e:
            print("Error Updating Cluster",e.__str__())
            raise HTTPException(status_code=400, detail="Unable to Update the Cluster")
            
    return capacity


def delete_capacity(profile_id:str, capacity_id: str, db:Session):
    obj = db.query(models.Capacity).filter(models.Capacity.id == capacity_id).filter(models.Capacity.ProfileId == profile_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return

