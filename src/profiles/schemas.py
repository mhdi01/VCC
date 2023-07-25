from schemas import *

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


class ProfileOut(BaseModel):
    id: str
    name: constr(min_length=1, max_length=127)
    ProfileTag: constr(min_length=1, max_length=127)
    ReservedAliases: set
    ProfileFQDN: constr(max_length=100)
    Status: bool
    RegistrationTime: datetime.date | None = None
    LastUpdateTime: datetime.date | None = None
    CreatedBy: str | None = None
    LastUpdateBy: str | None = None


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
