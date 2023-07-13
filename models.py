from typing import Any
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.types import ARRAY
import enum
from database import Base


class SeatTypeEnum(enum.Enum):
    VCRoom = 'VCRoom'
    VCHall = 'VCHall'
    VCClass = 'VCClass'
    VCVoice = 'VCVoice'
    VOIP = 'VOIP'

class HostViewEnum(enum.Enum):
    one_main_zero_pips = 'one_main_zero_pips'
    four_mains_zero_pips = 'four_mains_zero_pips'
    one_main_seven_pips = 'one_main_seven_pips'
    one_main_twentyone_pips = 'one_main_twentyone_pips'
    two_mains_twentyone_pips = 'two_mains_twentyone_pips'


class Cluster(Base):
    __tablename__ = "clusters"

    id = Column(String, primary_key=True, index=True)
    name = Column(String(length=127), index=True, nullable=False)
    SeatType = Column(Enum(SeatTypeEnum), nullable=False)
    MaxLimit = Column(Integer, nullable=False)
    DefaultFQDN = Column(String(length=100), nullable=False)
    DefaultSettingId = Column(String, ForeignKey("settings.id"))
    DefaultSetting = relationship("Setting", back_populates="settings")
    Status = Column(Boolean, nullable=False)
    RegistrationTime = Column(DateTime, nullable=True)
    LastUpdateTime = Column(DateTime, nullable=True)
    CreatedBy = Column(String(length=32), nullable=True)
    LastUpdateBy = Column(String(length=32), nullable=True)
    # Sqlalchemy Arary Field ?
    
    
    unique_together = (('DefaultFQDN', 'name'),)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, index=True)
    name = Column(String(length=127), index=True, nullable=False)
    ProfileTag = Column(String(length=127), nullable=False)
    ReservedAliases = Column(ARRAY(String), default=[], nullable=True)
    ProfileFQDN = Column(String(length=100), nullable=False)
    Status = Column(Boolean, nullable=True)
    RegistrationTime = Column(DateTime, nullable=True)
    LastUpdateTime = Column(DateTime, nullable=True)
    CreatedBy = Column(String(length=32), nullable=True)
    LastUpdateBy = Column(String(length=32), nullable=True)

    unique_together = (('ProfileTag', 'name'),)


class Setting(Base):
    __tablename__ = "settings"

    id = Column(String, primary_key=True, index=True)
    name = Column(String(length=127), index=True, nullable=False, unique=True)
    SeatType = Column(Enum(SeatTypeEnum), nullable=False)
    MaxCallRate = Column(Integer, nullable=False)
    OverlayText = Column(Boolean, nullable=False)
    HostView = Column(Enum(HostViewEnum), nullable=False)
    EnableChat = Column(Boolean, nullable=False)
    GuestsCanPresent = Column(Boolean, nullable=False)
    MuteAllGuests = Column(Boolean, nullable=False)
    IsDefault = Column(Boolean, nullable=True)
    Status = Column(Boolean, nullable=True)
    RegistrationTime = Column(DateTime, nullable=True)
    LastUpdateTime = Column(DateTime, nullable=True)
    CreatedBy = Column(String(length=32), nullable=True)
    LastUpdateBy = Column(String(length=32), nullable=True)

    settings = relationship("Cluster", back_populates="DefaultSetting")