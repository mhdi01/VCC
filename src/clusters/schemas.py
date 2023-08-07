from schemas import *


class ClusterBase(BaseModel):
    name: str
    SeatType: SeatTypeEnum
    MaxLimit: conint(gt=0, lt=500000)
    DefaultFQDN: constr(max_length=100)
    DefaultSettingId: str
    Status: bool
    MaintenanceStartTime: datetime.datetime | None = None
    MaintenanceEndTime: datetime.datetime | None = None
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None

class Cluster(ClusterBase):
    id: str | None = None

    class Config:
        from_attributes = True


class ClusterOut(BaseModel):
    id: str
    name: str
    SeatType: Optional[Enum] = Field(None, description="SeatType Has Issue")
    MaxLimit: conint(gt=0)
    DefaultFQDN: constr(max_length=100)
    DefaultSettingId: str 
    Status: bool
    MaintenanceStartTime: datetime.datetime | None = None
    MaintenanceEndTime: datetime.datetime | None = None
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None



class ClusterPatch(ClusterBase):
    name: str | None = None
    SeatType: SeatTypeEnum | None = None
    MaxLimit: conint(gt=0, lt=500000) | None = None
    DefaultFQDN: constr(max_length=100) | None = None
    DefaultSettingId: str | None = None
    Status: bool | None = None
    MaintenanceStartTime: datetime.datetime | None = None
    MaintenanceEndTime: datetime.datetime | None = None
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None

