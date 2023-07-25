from typing import Any, Optional, List
from pydantic import (
    BaseModel,
    NegativeInt,
    PositiveInt,
    conint,
    conlist,
    constr,
    conset,
    Field,
    Json
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


class PlanTypeEnum(str, Enum):
    Fixed = 'Fixed'
    Volume = 'Volume'
