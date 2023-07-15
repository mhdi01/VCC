from database import get_db
from . import schemas, crud
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, APIRouter

router = APIRouter(
    prefix="/api/Profiles",
    tags=["profiles"],
    dependencies=[Depends(get_db)]
)


@router.post("/")
def create_profile(profile: schemas.Profile, db: Session = Depends(get_db)):
    profile_obj = crud.get_profile_by_name_and_fqdn(name=profile.name, tag=profile.ProfileTag, db=db)
    if profile_obj:
        raise HTTPException(status_code=400, detail="Name already registered")
    
    resp = crud.create_profile(db=db, profile=profile)
    return resp

@router.get("/")
def read_profiles(db: Session = Depends(get_db)):
    resp = crud.get_profiles(db=db)
    return resp


@router.get("/{profile_id}")
def retrieve_profile(profile_id: str, db: Session = Depends(get_db)):
    resp = crud.retrieve_profile(profile_id=profile_id, db=db)
    return resp


@router.put("/{profile_id}")
def update_profile(profile_id: str, data:schemas.ProfileBase, db:Session = Depends(get_db)):
    resp = crud.update_profile(profile_id=profile_id, data=data, db=db)
    return resp


@router.patch("/{profile_id}")
def update_profile_partial(profile_id: str, data:schemas.ProfilePatch, db: Session = Depends(get_db)):
    resp = crud.update_profile(profile_id=profile_id, data=data, db=db)
    return resp

@router.delete("/{profile_id}", status_code=204)
def delete_profile(profile_id: str, db: Session = Depends(get_db)):
    crud.delete_profile(profile_id=profile_id, db=db)
    return 