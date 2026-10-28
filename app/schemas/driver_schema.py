from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from datetime import date

class DriverCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=10)
    dob: date | None = None
    joined_date: date
    license_number: str = Field(min_length=1, max_length=16)

class DriverUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=10)
    dob: date | None = None
    joined_date: date
    license_number: str = Field(min_length=1, max_length=16)

class DriverPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=20)
    dob: date | None = None
    joined_date: date | None = None
    license_number: str | None = Field(
        default=None, min_length=1, max_length=30
    )


class DriverResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str | None
    dob: date | None
    joined_date: date
    license_number: str


class DriverCollectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_number: str
    total_collection: Decimal
    net_collection: Decimal


class DriverWithCollectionsResponse(DriverResponse):
    collections: list[DriverCollectionResponse]