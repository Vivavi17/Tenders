"""Модуль схем валидации при работе с тендерами"""

import datetime
import uuid
from typing import Annotated, Literal, Optional

from pydantic import UUID4, AfterValidator, BaseModel


class TendersS(BaseModel):
    """Валидация ответов при работе с тендерами"""

    id: UUID4
    name: str
    description: str
    status: str
    serviceType: str
    version: int
    createdAt: datetime.datetime


class NewTenderS(BaseModel):
    """Валидация запроса при создании тендера"""

    name: str
    description: str
    serviceType: Literal["Construction", "Delivery", "Manufacture"]
    status: str = "Created"
    organizationId: (
        UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))]
    )
    creatorUsername: str


class EditTenderS(BaseModel):
    """Валидация запроса при редактировании тендера"""

    name: Optional[str] = None
    description: Optional[str] = None
    serviceType: Optional[Literal["Construction", "Delivery", "Manufacture"]] = None
