from datetime import date
from decimal import Decimal
from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class TransportCollection(Base):
    __tablename__ = "transport_collection"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True
    )
    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id", ondelete="CASCADE"), 
        nullable=False
    )

    # Many collection records belong to one driver.
    driver: Mapped["Driver"] = relationship(
        back_populates="collections"
    )

    vehicle_number: Mapped[str] = mapped_column(
        String(20), 
        nullable=False
    )

    collection_date: Mapped[date] = mapped_column(
        Date, 
        nullable=False
    )
    morning_trips: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )
    evening_trips: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )
    morning_collection: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), 
        nullable=False
    )
    evening_collection: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), 
        nullable=False
    )
    fuel_expense: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), 
        nullable=False
    )
    other_expense: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), 
        nullable=False
    )
    total_trips: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )
    total_collection: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), 
        nullable=False
    )
    total_expense: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), 
        nullable=False
    )
    net_collection: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), 
        nullable=False
    )
