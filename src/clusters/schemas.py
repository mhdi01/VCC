from schemas import *


class ClusterBase(BaseModel):
    name: str
    SeatType: SeatTypeEnum
    MaxLimit: conint(gt=0, lt=5000)
    DefaultFQDN: constr(max_length=100)
    DefaultSettingId: str
    Status: bool
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None

class Cluster(ClusterBase):
    id: str | None = None

    class Config:
        from_attributes = True

class ClusterPatch(ClusterBase):
    name: str | None = None
    SeatType: SeatTypeEnum | None = None
    MaxLimit: conint(gt=0, lt=5000) | None = None
    DefaultFQDN: constr(max_length=100) | None = None
    DefaultSettingId: str | None = None
    Status: bool | None = None
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None

