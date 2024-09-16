"""Модуль с существующими таблицами БД"""

import datetime
import uuid
from typing import Literal

from sqlalchemy import TIMESTAMP, DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from database import Base

organization_type = Literal["IE", "LLC", "JSC"] # pylint: disable=invalid-name


class Employee(Base): # pylint: disable=too-few-public-methods
    """Сущность пользователя (User)"""

    __tablename__ = "employee"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)

    created_at: Mapped[TIMESTAMP] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=True
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.utcnow,
        nullable=True,
        onupdate=datetime.datetime.utcnow,
    )
    # organizations: Mapped["OrganizationResponsible"] = relationship(back_populates="employee")
    # tenders: Mapped[list["Tenders"]] = relationship(back_populates="employee")
    # bids: Mapped[list["Bids"]] = relationship(back_populates="employee")


class Organization(Base): # pylint: disable=too-few-public-methods
    """Сущность организация (Organization)"""

    __tablename__ = "organization"

    id: Mapped[uuid.UUID] = mapped_column(
        server_default=text("uuid_generate_v4()"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[organization_type] = mapped_column(nullable=True)

    created_at: Mapped[TIMESTAMP] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.utcnow,
        server_default=func.now(), # pylint: disable=not-callable
        nullable=True,
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(), # pylint: disable=not-callable
        nullable=True,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    # responsible: Mapped["OrganizationResponsible"] = relationship(back_populates="organization")
    # tenders: Mapped[list["Tenders"]] = relationship(back_populates="organization")
    # bids: Mapped[list["Bids"]] = relationship(back_populates="organization")
    # feedback: Mapped["Feedback"] = relationship(back_populates="employee")


class OrganizationResponsible(Base): # pylint: disable=too-few-public-methods
    """Отношение пользователя к организаци"""

    __tablename__ = "organization_responsible"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"), nullable=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE"), nullable=True
    )

    # organization: Mapped["Organization"] = relationship(back_populates="responsible")
    # employee: Mapped["Employee"] = relationship(back_populates="organizations")
