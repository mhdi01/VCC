from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder


import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/Settings")
def create_setting(setting: schemas.Setting, db: Session = Depends(get_db)):
    setting_obj = crud.get_setting_by_name(name=setting.name, db=db)
    if setting_obj:
        raise HTTPException(status_code=400, detail="Name already registered")
    
    resp = crud.create_setting(db=db, setting=setting)
    return resp

@app.get("/api/Settings")
def read_setting(db: Session = Depends(get_db)):
    resp = crud.get_settings(db=db)
    return resp


@app.get("/api/Settings/{setting_id}")
def retrieve_setting(setting_id: str, db: Session = Depends(get_db)):
    resp = crud.retrieve_setting(setting_id=setting_id, db=db)
    return resp


@app.put("/api/Settings/{setting_id}")
def update_setting(setting_id: str, data:schemas.SettingBase, db:Session = Depends(get_db)):
    resp = crud.update_setting(setting_id=setting_id, data=data, db=db)
    return resp


@app.patch("/api/Settings/{setting_id}")
def update_setting_partial(setting_id: str, data:schemas.SettingPatch, db: Session = Depends(get_db)):
    resp = crud.update_setting(setting_id=setting_id, data=data, db=db)
    return resp

@app.delete("/api/Settings/{setting_id}", status_code=204)
def delete_setting(setting_id: str, db: Session = Depends(get_db)):
    crud.delete_setting(setting_id=setting_id, db=db)
    return 



@app.post("/api/Clusters")
def create_cluster(cluster: schemas.Cluster, db: Session = Depends(get_db)):
    cluster_obj = crud.get_cluster_by_name_and_fqdn(name=cluster.name, fqdn=cluster.DefaultFQDN, db=db)
    if cluster_obj:
        raise HTTPException(status_code=400, detail="Name already registered")
    
    resp = crud.create_cluster(db=db, cluster=cluster)
    return resp

@app.get("/api/Clusters")
def read_clusters(db: Session = Depends(get_db)):
    resp = crud.get_clusters(db=db)
    return resp


@app.get("/api/Clusters/{cluster_id}")
def retrieve_cluster(cluster_id: str, db: Session = Depends(get_db)):
    resp = crud.retrieve_cluster(cluster_id=cluster_id, db=db)
    return resp


@app.put("/api/Clusters/{cluster_id}")
def update_cluster(cluster_id: str, data:schemas.ClusterBase, db:Session = Depends(get_db)):
    resp = crud.update_cluster(cluster_id=cluster_id, data=data, db=db)
    return resp


@app.patch("/api/Clusters/{cluster_id}")
def update_cluster_partial(cluster_id: str, data:schemas.ClusterPatch, db: Session = Depends(get_db)):
    resp = crud.update_cluster(cluster_id=cluster_id, data=data, db=db)
    return resp

@app.delete("/api/Clusters/{cluster_id}", status_code=204)
def delete_cluster(cluster_id: str, db: Session = Depends(get_db)):
    crud.delete_cluster(cluster_id=cluster_id, db=db)
    return 



@app.post("/api/Profiles")
def create_profile(profile: schemas.Profile, db: Session = Depends(get_db)):
    profile_obj = crud.get_profile_by_name_and_fqdn(name=profile.name, tag=profile.ProfileTag, db=db)
    if profile_obj:
        raise HTTPException(status_code=400, detail="Name already registered")
    
    resp = crud.create_profile(db=db, profile=profile)
    return resp

@app.get("/api/Profiles")
def read_profiles(db: Session = Depends(get_db)):
    resp = crud.get_profiles(db=db)
    return resp


@app.get("/api/Profiles/{profile_id}")
def retrieve_profile(profile_id: str, db: Session = Depends(get_db)):
    resp = crud.retrieve_profile(profile_id=profile_id, db=db)
    return resp


@app.put("/api/Profiles/{profile_id}")
def update_profile(profile_id: str, data:schemas.ProfileBase, db:Session = Depends(get_db)):
    resp = crud.update_profile(profile_id=profile_id, data=data, db=db)
    return resp


@app.patch("/api/Profiles/{profile_id}")
def update_profile_partial(profile_id: str, data:schemas.ProfilePatch, db: Session = Depends(get_db)):
    resp = crud.update_profile(profile_id=profile_id, data=data, db=db)
    return resp

@app.delete("/api/Profiles/{profile_id}", status_code=204)
def delete_profile(profile_id: str, db: Session = Depends(get_db)):
    crud.delete_profile(profile_id=profile_id, db=db)
    return 