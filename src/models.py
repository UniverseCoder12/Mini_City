from __future__ import annotations

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship


class Base(DeclarativeBase):
    pass


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(150), nullable=False)
    seed: Mapped[int] = Column(Integer, default=0)
    width: Mapped[int] = Column(Integer, default=32)
    height: Mapped[int] = Column(Integer, default=32)
    money: Mapped[int] = Column(Integer, default=20000)
    day: Mapped[int] = Column(Integer, default=1)
    tax_rate: Mapped[int] = Column(Integer, default=9)
    negative_months: Mapped[int] = Column(Integer, default=0)
    game_over: Mapped[bool] = Column(Boolean, default=False)
    peak_population: Mapped[int] = Column(Integer, default=0)
    next_building_id: Mapped[int] = Column(Integer, default=1)
    next_event_id: Mapped[int] = Column(Integer, default=1)

    tiles: Mapped[list["Tile"]] = relationship(back_populates="city", cascade="all, delete-orphan")
    buildings: Mapped[list["Building"]] = relationship(back_populates="city", cascade="all, delete-orphan")
    city_stats: Mapped["CityStats | None"] = relationship(back_populates="city", uselist=False, cascade="all, delete-orphan")
    game_events: Mapped[list["GameEvent"]] = relationship(back_populates="city", cascade="all, delete-orphan")


class Tile(Base):
    __tablename__ = "tiles"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    city_id: Mapped[int] = Column(Integer, ForeignKey("cities.id"), nullable=False, index=True)
    x: Mapped[int] = Column(Integer, nullable=False)
    y: Mapped[int] = Column(Integer, nullable=False)
    terrain: Mapped[str] = Column(String(20), default="grass")
    road: Mapped[bool] = Column(Boolean, default=False)
    zone: Mapped[str] = Column(String(30), default="none")
    building_id: Mapped[int | None] = Column(Integer, ForeignKey("buildings.id"), nullable=True)
    near_road: Mapped[bool] = Column(Boolean, default=False)

    city: Mapped[City] = relationship(back_populates="tiles")
    building: Mapped["Building | None"] = relationship(back_populates="tiles")


class BuildingType(Base):
    __tablename__ = "building_types"

    id: Mapped[str] = Column(String(50), primary_key=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    category: Mapped[str] = Column(String(30), nullable=False)
    icon: Mapped[str] = Column(String(20), default="")
    width: Mapped[int] = Column(Integer, default=1)
    height: Mapped[int] = Column(Integer, default=1)
    build_cost: Mapped[int] = Column(Integer, default=0)
    upkeep: Mapped[int] = Column(Integer, default=0)
    capacity: Mapped[int] = Column(Integer, default=0)
    power_consumption: Mapped[int] = Column(Integer, default=0)
    power_production: Mapped[int] = Column(Integer, default=0)
    service_type: Mapped[str | None] = Column(String(30), nullable=True)
    effect_radius: Mapped[int] = Column(Integer, default=0)
    happiness_effect: Mapped[int] = Column(Integer, default=0)
    unlock_population: Mapped[int] = Column(Integer, default=0)

    buildings: Mapped[list["Building"]] = relationship(back_populates="building_type")


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    city_id: Mapped[int] = Column(Integer, ForeignKey("cities.id"), nullable=False, index=True)
    type_id: Mapped[str] = Column(String(50), ForeignKey("building_types.id"), nullable=False, index=True)
    x: Mapped[int] = Column(Integer, nullable=False)
    y: Mapped[int] = Column(Integer, nullable=False)
    level: Mapped[int] = Column(Integer, default=1)
    occupants: Mapped[int] = Column(Integer, default=0)
    built_day: Mapped[int] = Column(Integer, default=1)
    powered: Mapped[bool] = Column(Boolean, default=True)
    connected: Mapped[bool] = Column(Boolean, default=False)
    happiness: Mapped[int] = Column(Integer, default=50)
    days_happy: Mapped[int] = Column(Integer, default=0)
    days_unhappy: Mapped[int] = Column(Integer, default=0)
    on_fire: Mapped[bool] = Column(Boolean, default=False)
    abandoned: Mapped[bool] = Column(Boolean, default=False)

    city: Mapped[City] = relationship(back_populates="buildings")
    building_type: Mapped[BuildingType] = relationship(back_populates="buildings")
    tiles: Mapped[list[Tile]] = relationship(back_populates="building")
    events: Mapped[list["GameEvent"]] = relationship(back_populates="building")


class CityStats(Base):
    __tablename__ = "city_stats"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    city_id: Mapped[int] = Column(Integer, ForeignKey("cities.id"), unique=True, nullable=False, index=True)
    population: Mapped[int] = Column(Integer, default=0)
    working_age: Mapped[int] = Column(Integer, default=0)
    residential_capacity: Mapped[int] = Column(Integer, default=0)
    jobs_commercial: Mapped[int] = Column(Integer, default=0)
    jobs_industrial: Mapped[int] = Column(Integer, default=0)
    jobs: Mapped[int] = Column(Integer, default=0)
    workers: Mapped[int] = Column(Integer, default=0)
    unemployment: Mapped[float] = Column(Float, default=0.0)
    demand_residential: Mapped[int] = Column(Integer, default=0)
    demand_commercial: Mapped[int] = Column(Integer, default=0)
    demand_industrial: Mapped[int] = Column(Integer, default=0)
    happiness: Mapped[int] = Column(Integer, default=50)
    power_produced: Mapped[int] = Column(Integer, default=0)
    power_consumed: Mapped[int] = Column(Integer, default=0)
    blackout: Mapped[bool] = Column(Boolean, default=False)
    road_tiles: Mapped[int] = Column(Integer, default=0)
    income: Mapped[int] = Column(Integer, default=0)
    expenses: Mapped[int] = Column(Integer, default=0)
    balance: Mapped[int] = Column(Integer, default=0)

    city: Mapped[City] = relationship(back_populates="city_stats")


class GameEvent(Base):
    __tablename__ = "game_events"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    city_id: Mapped[int] = Column(Integer, ForeignKey("cities.id"), nullable=False, index=True)
    type: Mapped[str] = Column(String(30), nullable=False)
    day: Mapped[int] = Column(Integer, default=1)
    duration: Mapped[int] = Column(Integer, default=1)
    active: Mapped[bool] = Column(Boolean, default=True)
    building_id: Mapped[int | None] = Column(Integer, ForeignKey("buildings.id"), nullable=True)
    message: Mapped[str] = Column(String(255), default="")

    city: Mapped[City] = relationship(back_populates="game_events")
    building: Mapped["Building | None"] = relationship(back_populates="events")
