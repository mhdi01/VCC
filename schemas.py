from typing import Any
from pydantic import (
    BaseModel,
    NegativeInt,
    PositiveInt,
    conint,
    conlist,
    constr,
    conset
)
import datetime
from enum import Enum


class SeatTypeEnum(str, Enum):
    VCRoom = 'VCRoom'
    VCHall = 'VCHall'
    VCClass = 'VCClass'
    VCVoice = 'VCVoice'
    VOIP = 'VOIP'


class HostViewEnum(str, Enum):
    one_main_zero_pips = 'one_main_zero_pips'
    four_mains_zero_pips = 'four_mains_zero_pips'
    one_main_seven_pips = 'one_main_seven_pips'
    one_main_twentyone_pips = 'one_main_twentyone_pips'
    two_mains_twentyone_pips = 'two_mains_twentyone_pips'


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
        orm_mode = True


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



class ProfileBase(BaseModel):
    name: constr(min_length=1, max_length=127)
    ProfileTag: constr(min_length=1, max_length=127)
    ReservedAliases: set
    ProfileFQDN: constr(min_length=1, max_length=100)
    Status: bool | None = None
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None


class Profile(ProfileBase):
    id: str | None = None

    class Config:
        from_attributes = True


class ProfilePatch(ProfileBase):
    name: constr(min_length=1, max_length=127) | None = None
    ProfileTag: constr(min_length=1, max_length=127) | None = None
    ReservedAliases: set  | None = None
    ProfileFQDN: constr(min_length=1, max_length=100) | None = None
    Status: bool | None = None
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None
