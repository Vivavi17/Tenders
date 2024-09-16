"""Модели для работы с тендерами"""

import datetime
import uuid
from typing import Literal

from sqlalchemy import DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from database import Base


class Tenders(Base): # pylint: disable=too-few-public-methods
    """Модель контекста тендера"""

    __tablename__ = "tenders"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("version_tenders.id"))
    pk: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    serviceType: Mapped[Literal["Construction", "Delivery", "Manufacture"]] = (
        mapped_column(nullable=True)
    )
    status: Mapped[Literal["Created", "Published", "Closed"]] = mapped_column(
        nullable=True
    )
    organizationId: Mapped[uuid.UUID] = mapped_column(ForeignKey("organization.id"))
    creatorId: Mapped[uuid.UUID] = mapped_column(ForeignKey("employee.id"))
    createdAt: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True # pylint: disable=not-callable
    )
    version: Mapped[int] = mapped_column(default=1, server_default=text("1"))

    # tendersVersion: Mapped["VersionTenders"] = relationship(back_populates="tenders")
    # employee: Mapped["Employee"] = relationship(back_populates="tenders")
    # organization: Mapped["Organization"] = relationship(back_populates="tenders")
    # bids: Mapped["Bids"] = relationship(back_populates="tender")
    # feedback: Mapped["Feedback"] = relationship(back_populates="tender")


class VersionTenders(Base): # pylint: disable=too-few-public-methods
    """Модель хранения версии тендера"""

    __tablename__ = "version_tenders"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    version: Mapped[int] = mapped_column(default=1, server_default=text("1"))

    # tenders: Mapped[list["Tenders"]] = relationship(back_populates="tendersVersion")
