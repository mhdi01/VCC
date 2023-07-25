from database import get_db
from . import schemas, crud
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, APIRouter

router = APIRouter(
    prefix="/api/Profiles/{profile_id}/Capacities",
    tags=["capacities"],
    dependencies=[Depends(get_db)]
)


@router.post("/")
def create_capacity(profile_id: str, capacity: schemas.Capacity, db: Session = Depends(get_db)):
    resp = crud.create_capacity(db=db, capacity=capacity, profile_id=profile_id)
    return resp

@router.get("/", response_model=list[schemas.CapacityOut])
def read_capacities(profile_id: str, db: Session = Depends(get_db)):
    resp = crud.get_capacities(profile_id=profile_id ,db=db)
    return resp


@router.get("/{capacity_id}", response_model=schemas.CapacityOut)
def retrieve_capacity(profile_id: str, capacity_id: str, db: Session = Depends(get_db)):
    resp = crud.retrieve_capacity(profile_id, capacity_id=capacity_id, db=db)
    if not resp:
        raise HTTPException(status_code=404, detail='Capacity Not Found')
    return resp


@router.put("/{capacity_id}", response_model=schemas.CapacityOut)
def update_capacity(profile_id: str, capacity_id: str, data:schemas.CapacityBase, db:Session = Depends(get_db)):
    resp = crud.update_capacity(profile_id=profile_id, capacity_id=capacity_id, data=data, db=db)
    return resp


@router.patch("/{capacity_id}", response_model=schemas.CapacityOut)
def update_capacity_partial(profile_id:str, capacity_id: str, data:schemas.CapacityPatch, db: Session = Depends(get_db)):
    resp = crud.update_capacity(profile_id=profile_id, capacity_id=capacity_id, data=data, db=db)
    return resp


@router.delete("/{capacity_id}", status_code=204)
def delete_capacity(profile_id: str, capacity_id: str, db: Session = Depends(get_db)):
    crud.delete_capacity(profile_id=profile_id, capacity_id=capacity_id, db=db)
    return 
