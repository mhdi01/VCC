from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, FastAPI, HTTPException, APIRouter

import models
from . import schemas
from actions import id_generator, TableRepository
import time


def get_clusters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cluster).offset(skip).limit(limit).all()


def create_cluster(db: Session, cluster: schemas.Cluster):
    try:
        cluster.id = id_generator()
        try:
            cluster.MaintenanceStartTime = time.mktime(cluster.MaintenanceStartTime.timetuple())
            cluster.MaintenanceEndTime = time.mktime(cluster.MaintenanceEndTime.timetuple())
        except Exception as e:
            cluster.MaintenanceStartTime = None
            cluster.MaintenanceEndTime = None
            
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
    if not cluster:
        raise HTTPException(status_code=404, detail='Cluster Not found')
    if cluster:
        try:
            update_data = data.model_dump(exclude_unset=True)
            if 'MaintenanceStartTime' in update_data:
                update_data['MaintenanceStartTime'] = time.mktime(update_data['MaintenanceStartTime'].timetuple())

            if 'MaintenanceEndTime' in update_data:
                update_data['MaintenanceEndTime'] = time.mktime(update_data['MaintenanceEndTime'].timetuple())
            
            repo.set_attrs(cluster, update_data)
            db.commit()
            db.refresh(cluster)

        except Exception as e:
            print("Error Updating Cluster",e.__str__())
            raise HTTPException(status_code=400, detail="Unable to Update the Cluster")
            
    return cluster


def delete_cluster(cluster_id: str, db:Session):
    obj = db.query(models.Cluster).filter(models.Cluster.id == cluster_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return


def get_cluster_by_name_and_fqdn(name: str, fqdn: str, db:Session):
    return db.query(models.Cluster).filter(models.Cluster.name == name).filter(models.Cluster.DefaultFQDN == fqdn).first()
