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
