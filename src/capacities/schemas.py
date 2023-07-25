from schemas import *
from clusters.schemas import Cluster, ClusterBase

class CapacityBase(BaseModel):
    SeatType: SeatTypeEnum
    PlanType: PlanTypeEnum
    CapacityLimit: conint(gt=0, lt=500000)
    ProfileId: str | None = None
    ClusterId: str
    Status: bool
    StartTime: Optional[datetime.datetime] = Field(None, description="Start Time Data Type has issue")
    EndTime: Optional[datetime.datetime] = Field(None, description="End Time Data Type has issue")
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None


class CapacityOut(BaseModel):
    id: str
    SeatType: Optional[Enum] = Field(None, description="SeatType Has Issue")
    PlanType: Optional[Enum] = Field(None, description="PlanType Has Issue")
    CapacityLimit: conint(gt=0, lt=500000)
    ProfileId: str | None = None
    ClusterId: str
    Status: bool
    StartTime: Optional[float] = Field(None, description="Start Time Data Type has issue")
    EndTime: Optional[float] = Field(None, description="End Time Data Type has issue")
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None



class Capacity(CapacityBase):
    id: str | None = None    

    class Config:
        from_attributes = True

class CapacityPatch(CapacityBase):
    name: str | None = None
    SeatType: SeatTypeEnum | None = None
    PlanType: PlanTypeEnum | None = None
    CapacityLimit: conint(gt=0, lt=500000) | None = None
    ProfileId: str | None = None
    ClusterId: str | None = None
    Status: bool | None = None
    StartTime: Optional[datetime.datetime] = Field(None, description="Start Time Data Type has issue")
    EndTime: Optional[datetime.datetime] = Field(None, description="End Time Data Type has issue")
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None
