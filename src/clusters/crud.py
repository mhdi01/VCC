from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, FastAPI, HTTPException, APIRouter

import models
from . import schemas
from actions import id_generator, TableRepository


def get_clusters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cluster).offset(skip).limit(limit).all()


def create_cluster(db: Session, cluster: schemas.Cluster):
    try:
        cluster.id = id_generator()
        db_cluster = models.Cluster(**cluster.model_dump())
        db.add(db_cluster)
        db.commit()
        db.refresh(db_cluster)
    except Exception as e:
        print("Error creating Cluster",e.__str__())
        raise HTTPException(status_code=400, detail="Unable to Create the Cluster")
    
    return db_cluster


def retrieve_cluster(cluster_id: str, db:Session):
    return db.query(models.Cluster).filter(models.Cluster.id == cluster_id).first()


def update_cluster(cluster_id: str, data: schemas.ClusterBase, db:Session):
    repo = TableRepository(db, models.Cluster)
    cluster = repo.find_by_id(cluster_id)
    if cluster:
        try:
            update_data = data.model_dump(exclude_unset=True)
            repo.set_attrs(cluster, update_data)
            db.commit()
            db.refresh(cluster)

        except Exception as e:
            print("Error Updating Cluster",e.__str__())
            raise HTTPException(status_code=400, detail="Unable to Update the Cluster")
            
    return jsonable_encoder(cluster)


def delete_cluster(cluster_id: str, db:Session):
    obj = db.query(models.Cluster).filter(models.Cluster.id == cluster_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return


def get_cluster_by_name_and_fqdn(name: str, fqdn: str, db:Session):
    return db.query(models.Cluster).filter(models.Cluster.name == name).filter(models.Cluster.DefaultFQDN == fqdn).first()
