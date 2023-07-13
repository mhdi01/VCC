
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

import models, schemas
from actions import id_generator
from table_respository import TableRepository

def get_clusters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cluster).offset(skip).limit(limit).all()


def create_cluster(db: Session, cluster: schemas.Cluster):
    cluster.id = id_generator()
    db_cluster = models.Cluster(**cluster.model_dump())
    db.add(db_cluster)
    db.commit()
    db.refresh(db_cluster)
    return db_cluster


def retrieve_cluster(cluster_id: str, db:Session):
    return db.query(models.Cluster).filter(models.Cluster.id == cluster_id).first()


def update_cluster(cluster_id: str, data: schemas.ClusterBase, db:Session):
    repo = TableRepository(db, models.Cluster)
    cluster = repo.find_by_id(cluster_id)
    if cluster:
        update_data = data.model_dump(exclude_unset=True)
        repo.set_attrs(cluster, update_data)
        db.commit()
        db.refresh(cluster)
    return jsonable_encoder(cluster)


def delete_cluster(cluster_id: str, db:Session):
    obj = db.query(models.Cluster).filter(models.Cluster.id == cluster_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return


def get_cluster_by_name_and_fqdn(name: str, fqdn: str, db:Session):
    return db.query(models.Cluster).filter(models.Cluster.name == name).filter(models.Cluster.DefaultFQDN == fqdn).first()


def get_profile_by_name_and_fqdn(name: str, tag: str, db:Session):
    return db.query(models.Profile).filter(models.Profile.name == name).filter(models.Profile.ProfileTag == tag).first()


def create_profile(profile: schemas.Profile, db:Session):
    profile.id = id_generator()
    db_profile = models.Profile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profile).offset(skip).limit(limit).all()


def retrieve_profile(profile_id: str, db:Session):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()


def update_profile(profile_id: str, data:schemas.ProfileBase, db: Session):
    repo = TableRepository(db, models.Profile)
    profile = repo.find_by_id(profile_id)
    if profile:
        update_data = data.model_dump(exclude_unset=True)
        repo.set_attrs(profile, update_data)
        db.commit()
        db.refresh(profile)
    return jsonable_encoder(profile)


def delete_profile(profile_id: str, db: Session):
    obj = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return


def get_settings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Setting).offset(skip).limit(limit).all()

def get_setting_by_name(name: str, db:Session):
    return db.query(models.Setting).filter(models.Setting.name == name).first()


def retrieve_setting(setting_id: str, db:Session):
    return db.query(models.Setting).filter(models.Setting.id == setting_id).first()


def create_setting(db: Session, setting: schemas.Setting):
    setting.id = id_generator()
    db_setting = models.Setting(**setting.model_dump())
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting


def update_setting(setting_id: str, data:schemas.SettingBase, db: Session):
    repo = TableRepository(db, models.Setting)
    setting = repo.find_by_id(setting_id)
    if setting:
        update_data = data.model_dump(exclude_unset=True)
        repo.set_attrs(setting, update_data)
        db.commit()
        db.refresh(setting)
    return jsonable_encoder(setting)


def delete_setting(setting_id: str, db: Session):
    obj = db.query(models.Setting).filter(models.Setting.id == setting_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return