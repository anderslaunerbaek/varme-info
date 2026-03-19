import enum
from dataclasses import dataclass, field
from datetime import datetime

from .utils import create_uuid


class EmumType(enum.Enum):

    def __str__(self):
        return self.name


class HeatUnitType(EmumType):
    type1 = enum.auto()
    type2 = enum.auto()


class SensorRecordType(EmumType):
    type1 = enum.auto()
    type2 = enum.auto()


@dataclass
class HeatUnit:
    name: str
    type: HeatUnitType
    id: str = field(default_factory=create_uuid)


@dataclass
class SensorRecord:
    type: SensorRecordType
    value: float
    heat_unit_id: str
    correlation_id: str = field(default_factory=create_uuid)
    time_stamp: str = field(default_factory=datetime.now().isoformat)
