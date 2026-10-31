from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.driver_schema import DriverResponse

class CollectionFields(BaseModel):
    driver_id: int = Field(gt=0)
    vehicle_number: str = Field(min_length=1, max_length=20)
    collection_date: date
    morning_trips: int = Field(ge=0)
    evening_trips: int = Field(ge=0)
    morning_collection: Decimal = Field(ge=0)
    evening_collection: Decimal = Field(ge=0)
    fuel_expense: Decimal = Field(ge=0)
    other_expense: Decimal = Field(ge=0)

class CollectionCreate(BaseModel):
    driver_id: int = Field(gt=0)
    vehicle_number: str = Field(min_length=1, max_length=20)
    collection_date: date
    morning_trips: int = Field(ge=0)
    evening_trips: int = Field(ge=0)
    morning_collection: Decimal = Field(ge=0)
    evening_collection: Decimal = Field(ge=0)
    fuel_expense: Decimal = Field(ge=0)
    other_expense: Decimal = Field(ge=0)


class CollectionUpdate(BaseModel):
    driver_id: int | None = Field(default=None, gt=0)
    vehicle_number: str | None = Field(default=None, min_length=1, max_length=20)
    collection_date: date | None = None
    morning_trips: int | None = Field(default=None, ge=0)
    evening_trips: int | None = Field(default=None, ge=0)
    morning_collection: Decimal | None = Field(default=None, ge=0)
    evening_collection: Decimal | None = Field(default=None, ge=0)
    fuel_expense: Decimal | None = Field(default=None, ge=0)
    other_expense: Decimal | None = Field(default=None, ge=0)

class CollectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    driver_id: int
    driver: DriverResponse
    vehicle_number: str
    collection_date: date
    morning_trips: int
    evening_trips: int
    morning_collection: Decimal
    evening_collection: Decimal
    fuel_expense: Decimal
    other_expense: Decimal
    total_trips: int
    total_collection: Decimal
    total_expense: Decimal
    net_collection: Decimal


class PaginationMetadata(BaseModel):
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool
    next_page: int | None
    previous_page: int | None


class CollectionListResponse(BaseModel):
    items: list[CollectionResponse]
    pagination: PaginationMetadata