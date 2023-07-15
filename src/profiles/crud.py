from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, FastAPI, HTTPException, APIRouter

import models
from . import schemas
from actions import id_generator, TableRepository


def get_profile_by_name_and_fqdn(name: str, tag: str, db:Session):
    return db.query(models.Profile).filter(models.Profile.name == name).filter(models.Profile.ProfileTag == tag).first()


def create_profile(profile: schemas.Profile, db:Session):
    try:
        profile.id = id_generator()
        db_profile = models.Profile(**profile.dict())
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
    
    except Exception as e:
        print("Error creating Profile",e.__str__())
        raise HTTPException(status_code=400, detail="Unable to Create the Profile")
    
    return db_profile


def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profile).offset(skip).limit(limit).all()


def retrieve_profile(profile_id: str, db:Session):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()


def update_profile(profile_id: str, data:schemas.ProfileBase, db: Session):
    repo = TableRepository(db, models.Profile)
    profile = repo.find_by_id(profile_id)
    if profile:
        try:
            update_data = data.model_dump(exclude_unset=True)
            repo.set_attrs(profile, update_data)
            db.commit()
            db.refresh(profile)
        except Exception as e:
            print("Error updating Profile",e.__str__())
            raise HTTPException(status_code=400, detail="Unable to Update the Profile")
        
    return jsonable_encoder(profile)


def delete_profile(profile_id: str, db: Session):
    obj = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return
