"""Response models. FastAPI turns these into the OpenAPI spec."""

from datetime import date
from typing import Literal

from pydantic import BaseModel

UnitBasis = Literal["kg", "L", "each"]
PriceType = Literal["sale", "regular"]
SourceType = Literal["flyer", "receipt", "in_store"]


class ItemSummary(BaseModel):
    id: int
    name: str
    category: str | None
    observation_count: int
    latest_store: str | None
    latest_observed_on: date | None
    latest_price: float | None
    latest_unit_price: float | None
    unit_basis: UnitBasis | None


class PricePoint(BaseModel):
    observed_on: date
    store: str
    price: float
    unit_price: float
    unit_basis: UnitBasis
    price_type: PriceType
    source_type: SourceType


class PriceStats(BaseModel):
    unit_basis: UnitBasis
    observation_count: int
    min_unit_price: float
    median_unit_price: float
    max_unit_price: float
    latest_unit_price: float


class ItemDetail(BaseModel):
    id: int
    name: str
    category: str | None
    stats: PriceStats | None
    prices: list[PricePoint]
