from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.transport_collection_model import TransportCollection


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    phone: Mapped[str | None] = mapped_column(
        String(10), unique=True
    )

    dob: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )
    joined_date: Mapped[date] = mapped_column(
        Date, nullable=False
    )
    license_number: Mapped[str] = mapped_column(
        String(16), unique=True, nullable=False
    )

    address: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    # One driver can have many collection records.

    collections: Mapped[list["TransportCollection"]] = relationship(
        back_populates="driver",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
