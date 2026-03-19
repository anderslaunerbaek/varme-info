from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy import Enum as SAEnum
from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .data import HeatUnitType
from .utils import create_uuid


class Base(DeclarativeBase):
    pass


class HeatUnitModel(Base):
    __tablename__ = "heat_units"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=create_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[HeatUnitType] = mapped_column(SAEnum(HeatUnitType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user_heat_units: Mapped[List["UserHeatUnitModel"]] = relationship("UserHeatUnitModel", back_populates="heat_unit")


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=create_uuid)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    heat_units: Mapped[List["UserHeatUnitModel"]] = relationship("UserHeatUnitModel", back_populates="user")


class UserHeatUnitModel(Base):
    __tablename__ = "user_heat_units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    heat_unit_id: Mapped[str] = mapped_column(String(36), ForeignKey("heat_units.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="heat_units")
    heat_unit: Mapped["HeatUnitModel"] = relationship("HeatUnitModel", back_populates="user_heat_units")
