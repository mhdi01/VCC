from typing import Any
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, ARRAY, Float
from sqlalchemy.orm import relationship
from sqlalchemy.types import ARRAY, Double
import enum
from database import Base
import datetime


from sqlalchemy.types import TypeDecorator


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


class PlanTypeEnum(enum.Enum):
    Fixed = 'Fixed'
    Volume = 'Volume'


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
    
    ClusterCapacity = relationship("Capacity", back_populates='CapacityCluster')
    ClusterSchedule = relationship("Schedule", back_populates="ScheduleCluster")
    
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


    ProfileCapacity = relationship("Capacity", back_populates="CapacityProfile")

    ProfileSchedule = relationship("Schedule", back_populates="ScheduleProfile")

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



class Capacity(Base):
    __tablename__ = 'capacities'

    id = Column(String, primary_key=True, index=True)
    PlanType = Column(Enum(PlanTypeEnum), nullable=False)
    SeatType = Column(Enum(SeatTypeEnum), nullable=False)
    CapacityLimit = Column(Integer, nullable=False)
    StartTime = Column(Float, nullable=False)
    EndTime = Column(Float, nullable=False)
    Status = Column(Boolean, nullable=True)
    RegistrationTime = Column(DateTime, nullable=True)
    LastUpdateTime = Column(DateTime, nullable=True)
    CreatedBy = Column(String(length=32), nullable=True)
    LastUpdateBy = Column(String(length=32), nullable=True)

    ProfileId = Column(String, ForeignKey("profiles.id"))
    CapacityProfile = relationship("Profile", back_populates="ProfileCapacity")

    ClusterId = Column(String, ForeignKey("clusters.id"))
    CapacityCluster = relationship("Cluster", back_populates="ClusterCapacity")

    CapacitySchedule = relationship("Schedule", back_populates="ScheduleCapacity")


class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(String, primary_key=True, index=True)
    Conference = Column(String(length=50), nullable=False)
    SeatType = Column(Enum(SeatTypeEnum), nullable=False)
    SeatLimit = Column(Integer, nullable=False)
    StartTime = Column(Float, nullable=False)
    EndTime = Column(Float, nullable=False)
    Status = Column(Boolean, nullable=True)
    RegistrationTime = Column(DateTime, nullable=True)
    LastUpdateTime = Column(DateTime, nullable=True)
    CreatedBy = Column(String(length=32), nullable=True)
    LastUpdateBy = Column(String(length=32), nullable=True)


    ProfileId = Column(String, ForeignKey("profiles.id"))
    ScheduleProfile = relationship("Profile", back_populates="ProfileSchedule")

    ClusterId = Column(String, ForeignKey("clusters.id"))
    ScheduleCluster = relationship("Cluster", back_populates="ClusterSchedule")

    CapacityId = Column(String, ForeignKey("capacities.id"))
    ScheduleCapacity = relationship("Capacity", back_populates="CapacitySchedule")

    