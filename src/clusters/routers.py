from database import get_db
from . import schemas, crud
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, APIRouter

router = APIRouter(
    prefix="/api/Clusters",
    tags=["clusters"],
    dependencies=[Depends(get_db)]
)


@router.post("/")
def create_cluster(cluster: schemas.Cluster, db: Session = Depends(get_db)):
    cluster_obj = crud.get_cluster_by_name_and_fqdn(name=cluster.name, fqdn=cluster.DefaultFQDN, db=db)
    if cluster_obj:
        raise HTTPException(status_code=400, detail="Name already registered")
    
    resp = crud.create_cluster(db=db, cluster=cluster)
    return resp

@router.get("/")
def read_clusters(db: Session = Depends(get_db)):
    resp = crud.get_clusters(db=db)
    return resp


@router.get("/{cluster_id}")
def retrieve_cluster(cluster_id: str, db: Session = Depends(get_db)):
    resp = crud.retrieve_cluster(cluster_id=cluster_id, db=db)
    return resp


@router.put("/{cluster_id}")
def update_cluster(cluster_id: str, data:schemas.ClusterBase, db:Session = Depends(get_db)):
    resp = crud.update_cluster(cluster_id=cluster_id, data=data, db=db)
    return resp


@router.patch("/{cluster_id}")
def update_cluster_partial(cluster_id: str, data:schemas.ClusterPatch, db: Session = Depends(get_db)):
    resp = crud.update_cluster(cluster_id=cluster_id, data=data, db=db)
    return resp

@router.delete("/{cluster_id}", status_code=204)
def delete_cluster(cluster_id: str, db: Session = Depends(get_db)):
    crud.delete_cluster(cluster_id=cluster_id, db=db)
    return 
