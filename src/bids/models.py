"""Модели таблиц для работы с предложениями и отзывами"""

import datetime
import uuid
from typing import Literal

from sqlalchemy import DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from database import Base


class Bids(Base):
    """Модель таблицы для работы с предложениями"""

    __tablename__ = "bids"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("version_bids.id"))
    pk: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    status: Mapped[Literal["Created", "Published", "Canceled"]] = mapped_column(
        default="Created", nullable=True
    )
    tenderId: Mapped[uuid.UUID] = mapped_column(ForeignKey("version_tenders.id"))
    authorId: Mapped[uuid.UUID] = mapped_column(ForeignKey("employee.id"))
    authorType: Mapped[Literal["Organization", "User"]]
    createdAt: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True # pylint: disable=all
    )
    version: Mapped[int] = mapped_column(default=1, server_default=text("1"))
    decision_count: Mapped[int] = mapped_column(default=0)

    # bidsVersion: Mapped["VersionBids"] = relationship(back_populates="bids")
    # employee: Mapped["Employee"] = relationship(back_populates="bids")
    # organization: Mapped["Organization"] = relationship(back_populates="bids")
    # tender: Mapped["Tender"] = relationship(back_populates="bids")


class VersionBids(Base):
    """Модель таблицы для хранения версии предложения"""

    __tablename__ = "version_bids"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    version: Mapped[int] = mapped_column(default=1, server_default=text("1"))
    # bids: Mapped[list["Bids"]] = relationship(back_populates="bidsVersion")


class Feedback(Base):
    """Модель таблицы для работы с отзывами"""

    __tablename__ = "feedback"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    tenderId: Mapped[int] = mapped_column(ForeignKey("version_tenders.id"))
    bidFeedback: Mapped[str]
    creatorUsername: Mapped[int] = mapped_column(ForeignKey("employee.username"))
    createdAt: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    authorId: Mapped[int] = mapped_column(ForeignKey("employee.id"))

    # tender: Mapped["Tender"] = relationship(back_populates="feedback")
    # employee: Mapped["Employee"] = relationship(back_populates="feedback")
