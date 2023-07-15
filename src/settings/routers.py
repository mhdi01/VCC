from database import get_db
from . import schemas, crud
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, APIRouter

router = APIRouter(
    prefix="/api/Settings",
    tags=["settings"],
    dependencies=[Depends(get_db)]
)

@router.post("/")
def create_setting(setting: schemas.Setting, db: Session = Depends(get_db)):
    setting_obj = crud.get_setting_by_name(name=setting.name, db=db)
    if setting_obj:
        raise HTTPException(status_code=400, detail="Name already registered")
    
    resp = crud.create_setting(db=db, setting=setting)
    return resp

@router.get("/")
def read_setting(db: Session = Depends(get_db)):
    resp = crud.get_settings(db=db)
    return resp


@router.get("/{setting_id}")
def retrieve_setting(setting_id: str, db: Session = Depends(get_db)):
    resp = crud.retrieve_setting(setting_id=setting_id, db=db)
    return resp


@router.put("/{setting_id}")
def update_setting(setting_id: str, data:schemas.SettingBase, db:Session = Depends(get_db)):
    resp = crud.update_setting(setting_id=setting_id, data=data, db=db)
    return resp


@router.patch("/{setting_id}")
def update_setting_partial(setting_id: str, data:schemas.SettingPatch, db: Session = Depends(get_db)):
    resp = crud.update_setting(setting_id=setting_id, data=data, db=db)
    return resp

@router.delete("/{setting_id}", status_code=204)
def delete_setting(setting_id: str, db: Session = Depends(get_db)):
    crud.delete_setting(setting_id=setting_id, db=db)
    return 

