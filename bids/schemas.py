"""Схемы моделей валидации для предложений фидбека и версий предложений"""

import datetime
import uuid
from typing import Annotated, Literal, Optional

from pydantic import UUID4, AfterValidator, BaseModel, Field


class NewBidsS(BaseModel):
    """Валидация при создании нового предложения"""

    name: str
    description: str
    tenderId: UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))]
    authorType: str
    authorId: UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))]


class BidsS(BaseModel):
    """Валидация ответов ендпоинтов"""

    id: UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))]
    name: str
    description: str
    status: Literal["Created", "Published", "Canceled"]
    authorType: Literal["Organization", "User"]
    authorId: UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))]
    version: int
    createdAt: datetime.datetime


class EditBidsS(BaseModel):
    """Валидация запроса на изменение предложения"""

    name: Optional[str] = None
    description: Optional[str] = None


class FeedbackS(BaseModel):
    """Валидация на создание фидбкека"""

    id: UUID4 = Field(validation_alias="tenderId")
    description: str = Field(validation_alias="bidFeedback")
    createdAt: datetime.datetime
