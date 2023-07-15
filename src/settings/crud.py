from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

import models
from . import schemas
from actions import id_generator, TableRepository

def get_settings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Setting).offset(skip).limit(limit).all()

def get_setting_by_name(name: str, db:Session):
    return db.query(models.Setting).filter(models.Setting.name == name).first()


def retrieve_setting(setting_id: str, db:Session):
    return db.query(models.Setting).filter(models.Setting.id == setting_id).first()


def create_setting(db: Session, setting: schemas.Setting):
    try:
        setting.id = id_generator()
        db_setting = models.Setting(**setting.model_dump())
        db.add(db_setting)
        db.commit()
        db.refresh(db_setting)
    except Exception as e:
        print("Error creating Setting",e.__str__())
        raise HTTPException(status_code=400, detail="Unable to Create the Setting")
    return db_setting


def update_setting(setting_id: str, data:schemas.SettingBase, db: Session):
    repo = TableRepository(db, models.Setting)
    setting = repo.find_by_id(setting_id)
    if setting:
        try:
            update_data = data.model_dump(exclude_unset=True)
            repo.set_attrs(setting, update_data)
            db.commit()
            db.refresh(setting)
        except Exception as e:
            print("Error updating Setting",e.__str__())
            raise HTTPException(status_code=400, detail="Unable to Update the Setting")
    return jsonable_encoder(setting)


def delete_setting(setting_id: str, db: Session):
    obj = db.query(models.Setting).filter(models.Setting.id == setting_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return