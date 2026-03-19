from sqlalchemy import Enum as SAEnum
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .data import HeatUnitType
from .utils import create_uuid


class Base(DeclarativeBase):
    pass


class HeatUnitModel(Base):
    __tablename__ = "heat_units"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=create_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[HeatUnitType] = mapped_column(SAEnum(HeatUnitType), nullable=False)
