from database import get_db
from . import schemas, crud
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, APIRouter

router = APIRouter(
    prefix="/api/Profiles/{profile_id}/Capacities/{capacity_id}",
    tags=["schedules"],
    dependencies=[Depends(get_db)]
)


@router.post("/Schedules/", response_model=schemas.ScheduleOut)
def create_schedule(profile_id: str, capacity_id: str, schedule: schemas.Schedule, db: Session = Depends(get_db)):
    resp = crud.book_schedule(db=db, schedule=schedule, capacity_id=capacity_id, profile_id=profile_id)
    return resp

@router.get("/Schedules/", response_model=list[schemas.ScheduleOut])
def read_schedules(profile_id: str, capacity_id: str, db: Session = Depends(get_db)):
    resp = crud.get_schedules(profile_id=profile_id , capacity_id=capacity_id, db=db)
    return resp


@router.get("/Schedules/{schedule_id}/", response_model=schemas.ScheduleOut)
def retrieve_schedule(profile_id: str, capacity_id: str, schedule_id: str, db: Session = Depends(get_db)):
    resp = crud.retrieve_schedule(profile_id=profile_id, capacity_id=capacity_id, schedule_id=schedule_id ,db=db)
    if not resp:
        raise HTTPException(status_code=404, detail='Schedule Not Found')
    return resp


@router.put("/Schedules/{schedule_id}/", response_model=schemas.ScheduleOut)
def update_schedule(profile_id: str, capacity_id: str, schedule_id:str, data:schemas.ScheduleBase, db:Session = Depends(get_db)):
    resp = crud.update_schedule(profile_id=profile_id, capacity_id=capacity_id, schedule_id=schedule_id, data=data, db=db)
    return resp


@router.patch("/Schedules/{schedule_id}/", response_model=schemas.ScheduleOut)
def update_schedule_partial(profile_id:str, capacity_id: str, schedule_id: str, data:schemas.SchedulePatch, db: Session = Depends(get_db)):
    resp = crud.update_schedule(profile_id=profile_id, capacity_id=capacity_id,  schedule_id=schedule_id, data=data, db=db)
    return resp


@router.delete("/Schedules/{schedule_id}/", status_code=204)
def delete_schedule(profile_id: str, capacity_id: str, schedule_id: str, db: Session = Depends(get_db)):
    crud.delete_schedule(profile_id=profile_id, capacity_id=capacity_id, schedule_id=schedule_id, db=db)
    return 
