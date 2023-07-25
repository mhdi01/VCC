from schemas import *


class ScheduleBase(BaseModel):
    SeatType: SeatTypeEnum
    Conference: constr(min_length=1)
    SeatLimit: conint(gt=0, lt=500000)
    ProfileId: str | None = None
    ClusterId: str
    CapacityId: str | None = None
    Status: bool
    StartTime: Optional[datetime.datetime] = Field(None, description="Start Time Data Type has issue")
    EndTime: Optional[datetime.datetime] = Field(None, description="End Time Data Type has issue")
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None

class Schedule(ScheduleBase):
    id: str | None = None
    

    class Config:
        from_attributes = True


class ScheduleOut(BaseModel):
    id: str
    Conference: constr(min_length=1)
    SeatLimit: conint(gt=0, lt=500000)
    SeatType: Optional[Enum] = Field(None, description="SeatType Has Issue")
    ProfileId: str | None = None
    ClusterId: str
    CapacityId: str | None = None
    Status: bool
    StartTime: Optional[float] = Field(None, description="Start Time Data Type has issue")
    EndTime: Optional[float] = Field(None, description="End Time Data Type has issue")
    RegistrationTime: datetime.datetime | None = None
    LastUpdateTime: datetime.datetime | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None


class SchedulePatch(ScheduleBase):
    SeatType: SeatTypeEnum | None = None
    Conference: constr(min_length=1) | None = None
    SeatLimit: conint(gt=0, lt=500000) | None = None
    ProfileId: str | None = None
    ClusterId: str | None = None
    CapacityId: str | None = None
    Status: bool | None = None
    StartTime: Optional[datetime.datetime] = Field(None, description="Start Time Data Type has issue")
    EndTime: Optional[datetime.datetime] = Field(None, description="End Time Data Type has issue")
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None
