"""Модуль бизнес-логики работы тендеров"""

from typing import Literal, Optional

from pydantic import UUID4

from exceptions import TenderDoesntExistException
from model_service import find_organization, find_user, is_user_responsible
from tenders.dao import TendersDAO, VersionTendersDAO
from tenders.schemas import NewTenderS, TendersS


async def find_tender(tender_id: UUID4):
    """Поиск тендера по id"""
    v = await VersionTendersDAO.find_one_or_none(id=tender_id)
    if not v:
        raise TenderDoesntExistException
    tender = await TendersDAO.find_one_or_none(id=tender_id, version=v.version)
    return tender


async def find_tenders(
    limit: int,
    offset: int,
    service_type: Optional[Literal["Construction", "Delivery", "Manufacture"]] = None,
) -> list[TendersS]:
    """Поиск Published тендеров по фильтру service_type с пагинацией"""
    tenders = await TendersDAO.find_all(
        limit, offset, serviceType=service_type, status="Published"
    )
    return tenders


async def create_new_tender(tender: NewTenderS):
    """Создать новый тендер"""
    await find_organization(id=tender.organizationId)
    user = await is_user_responsible(tender.creatorUsername, tender.organizationId)

    if user:
        id_version = await VersionTendersDAO.add()
        tender = await TendersDAO.add(
            id=id_version.id,
            name=tender.name,
            description=tender.description,
            serviceType=tender.serviceType,
            status=tender.status,
            organizationId=tender.organizationId,
            creatorId=user.id,
        )
        return tender


async def find_users_tenders(username: str, limit: int, offset: int) -> list[TendersS]:
    """Поиск тендеров созданных пользователем"""
    user = await find_user(username=username)
    tenders = await TendersDAO.find_all(limit, offset, creatorId=user.id)
    return tenders


async def get_status_tender(tender_id: UUID4, username: str):
    """Получение статуса тендера"""
    tender = await find_tender(tender_id)
    if tender.status == "Published":
        return tender.status
    await is_user_responsible(username, tender.organizationId)
    return tender.status


async def edit_status_tender(tender_id: UUID4, status: str, username: str):
    """Изменение статуса тендера"""
    tender = await find_tender(tender_id)
    await is_user_responsible(username, tender.organizationId)
    edited_tender = await TendersDAO.update_status(
        tender.id, tender.version, status=status
    )
    return edited_tender


async def edit_tender(tender_id: UUID4, username: str, data: dict):
    """Изменение данных тендера организацией"""
    tender = await find_tender(tender_id)
    await is_user_responsible(username, tender.organizationId)
    await VersionTendersDAO.update(tender_id, version=tender.version + 1)
    data = {k: v for k, v in data.items() if v is not None}
    tender = dict(tender)
    tender["version"] += 1
    tender.update(data)
    tender.pop("pk")
    edited_tender = await TendersDAO.add(**tender)
    return edited_tender


async def rollback_tender(tender_id: UUID4, version: int, username: str):
    """Откат версии тендера"""
    tender = await find_tender(tender_id)
    await is_user_responsible(username, tender.organizationId)
    versioned_tender = await TendersDAO.find_one_or_none(id=tender.id, version=version)
    if not versioned_tender:
        raise TenderDoesntExistException

    await VersionTendersDAO.update(tender_id, version=tender.version + 1)
    versioned_tender = dict(versioned_tender)
    versioned_tender["version"] = tender.version + 1
    versioned_tender.pop("pk")
    edited_tender = await TendersDAO.add(**versioned_tender)

    return edited_tender
