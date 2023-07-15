from schemas import *

class SettingBase(BaseModel):
    name: constr(min_length=1, max_length=127)
    SeatType: SeatTypeEnum
    MaxCallRate: conint(gt=10, lt=10000)
    OverlayText: bool
    HostView: HostViewEnum
    EnableChat: bool
    GuestsCanPresent: bool
    MuteAllGuests: bool
    IsDefault: bool| None = None
    Status: bool | None = None
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None


class Setting(SettingBase):
    id: str | None = None

    class Config:
        from_attributes = True


class SettingPatch(SettingBase):
    name: constr(min_length=1, max_length=127) | None = None
    SeatType: SeatTypeEnum | None = None
    MaxCallRate: conint(gt=10, lt=10000) | None = None
    OverlayText: bool | None = None
    HostView: HostViewEnum | None = None
    EnableChat: bool | None = None
    GuestsCanPresent: bool | None = None
    MuteAllGuests: bool | None = None
    IsDefault: bool| None = None
    Status: bool | None = None
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None

