"""Модуль ендпоинтов роутера /tenders"""
# pylint: disable=invalid-name

from typing import Literal, Optional

from fastapi import APIRouter
from pydantic import UUID4

from tenders.schemas import EditTenderS, NewTenderS, TendersS
from tenders.service import (
    create_new_tender,
    edit_status_tender,
    edit_tender,
    find_tenders,
    find_users_tenders,
    get_status_tender,
    rollback_tender,
)

router = APIRouter(prefix="/tenders")


@router.get("")
async def get_tenders(
    limit: int = 5,
    offset: int = 0,
    service_type: Optional[Literal["Construction", "Delivery", "Manufacture"]] = None,
) -> list[TendersS]:
    """Получение тендеров"""
    return await find_tenders(limit, offset, service_type)


@router.post("/new")
async def create_tender(tender: NewTenderS) -> TendersS:
    """Создание тендера"""
    return await create_new_tender(tender)


@router.get("/my")
async def get_users_tenders(
    username: str, limit: int = 5, offset: int = 0
) -> list[TendersS]:
    """Получение последних версий тендеров, созданных пользователем"""
    return await find_users_tenders(username, limit, offset)


@router.get("/{tenderId}/status")
async def get_status(tenderId: UUID4, username: Optional[str] = None) -> str:
    """Получение статуса тендера"""
    return await get_status_tender(tenderId, username)


@router.put("/{tenderId}/status")
async def edit_status(
    tenderId: UUID4, status: Literal["Created", "Published", "Closed"], username: str
) -> TendersS:
    """Изменение статуса тендера"""
    return await edit_status_tender(tenderId, status, username)


@router.patch("/{tenderId}/edit")
async def edit_tender_by_id(
    tenderId: UUID4, username: str, data: EditTenderS
) -> TendersS:
    """Изменение данных тендера"""
    return await edit_tender(tenderId, username, dict(data))


@router.put("/{tenderId}/rollback/{version}")
async def rollback_tender_by_id(tenderId: UUID4, version: int, username: str):
    """Откат версии тендера"""
    return await rollback_tender(tenderId, version, username)
