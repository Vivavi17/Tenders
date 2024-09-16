"""Бизнес-логика работы предложений и фидбека"""

from pydantic import UUID4

from bids.dao import BidsDAO, FeedbackDAO, VersionBidsDAO
from bids.schemas import BidsS, NewBidsS
from exceptions import BidDoesntExistException, UserDoesntHaveRightsException
from model_service import (
    count_responsible_user,
    find_user,
    is_user_in_organization,
    is_user_responsible,
)
from tenders.dao import TendersDAO
from tenders.service import find_tender


async def find_bid(bid_id: str):
    """Поиск предложений по id"""
    version = await VersionBidsDAO.find_one_or_none(id=bid_id)
    if not version:
        raise BidDoesntExistException
    bid = await BidsDAO.find_one_or_none(id=bid_id, version=version.version)
    return bid


async def is_user_author(bid_id: UUID4, username: str):
    """Проверка пользователя на авторство предложения"""
    bid = await find_bid(bid_id)
    user = await find_user(username=username)
    if bid.authorId != user.id:
        raise UserDoesntHaveRightsException
    return bid, user


async def create_new_bid(bid: NewBidsS):
    """Создание нового предложения"""
    if bid.authorType == "Organization":
        await is_user_in_organization(id=bid.authorId)
    else:
        await find_user(id=bid.authorId)
    tender = await find_tender(bid.tenderId)
    if tender.status == "Published":
        id_version = await VersionBidsDAO.add()
        bid = await BidsDAO.add(
            id=id_version.id,
            name=bid.name,
            description=bid.description,
            tenderId=bid.tenderId,
            authorId=bid.authorId,
            authorType=bid.authorType,
        )
        return bid


async def find_users_bids(
    username: str, limit: int = 5, offset: int = 0
) -> list[BidsS]:
    """Поиск всех предложений пользователя"""
    user = await find_user(username=username)
    bids = await BidsDAO.find_all(limit, offset, authorId=user.id)
    return bids


async def find_tenders_bids(tender_id: UUID4, username: str, limit: int, offset: int):
    """Поиск всех предложений тендера"""
    tender = await find_tender(tender_id)
    await is_user_responsible(username, tender.organizationId)
    bids = await BidsDAO.find_all(limit, offset, tenderId=tender_id)
    return bids


async def get_status_bid(bid_id: UUID4, username: str):
    """Получение статуса предложения автору или организации"""
    bid = await find_bid(bid_id)
    user = await find_user(username=username)
    if bid.authorId == user.id:
        return bid.status
    tender = await find_tender(bid.tenderId)
    if await is_user_responsible(username, tender.organizationId):
        return bid.status


async def edit_status_bid(bid_id: UUID4, status: str, username: str):
    """Изменить статус предложения (для автора)"""
    bid, _ = await is_user_author(bid_id, username)
    edited_bid = await BidsDAO.update_status(bid.id, bid.version, status=status)
    return edited_bid


async def edit_bid(bid_id: UUID4, username: str, data: dict):
    """Изменить данные в предложении"""
    bid, _ = await is_user_author(bid_id, username)
    await VersionBidsDAO.update(bid_id, version=bid.version + 1)
    data = {k: v for k, v in data.items() if v is not None}
    bid = dict(bid)
    bid["version"] += 1
    bid["decision_count"] = 0
    bid["status"] = "Created"
    bid.update(data)
    bid.pop("pk")
    edited_bid = await BidsDAO.add(**bid)
    return edited_bid


async def rollback_bid(bid_id: UUID4, version: int, username: str):
    """Откат версии предложения"""
    bid, _ = await is_user_author(bid_id, username)
    versioned_bid = await BidsDAO.find_one_or_none(id=bid.id, version=version)
    if not versioned_bid:
        raise BidDoesntExistException
    await VersionBidsDAO.update(bid.id, version=bid.version + 1)
    versioned_bid = dict(versioned_bid)
    versioned_bid["version"] = bid.version + 1
    versioned_bid.pop("pk")
    edited_bid = await BidsDAO.add(**versioned_bid)
    return edited_bid


async def submit_user_decision(bid_id: UUID4, decision: str, username: str):
    """Дать решение по предложению (только для организации тендера)"""
    bid = await find_bid(bid_id)
    tender = await find_tender(bid.tenderId)
    await is_user_responsible(username, tender.organizationId)
    if decision == "Approved":
        edited_bid = await BidsDAO.update(bid.pk, decision_count=bid.decision_count + 1)
        count = await count_responsible_user(tender.organizationId)
        if bid.decision_count + 1 >= min(3, count):
            await TendersDAO.update(tender.pk, status="Closed")
    else:
        edited_bid = await BidsDAO.update(bid.pk, status="Canceled")
    return edited_bid


async def add_feedback(bid_id: UUID4, bid_feedback: str, username: str):
    """Оставить фидбек на предложение"""
    bid = await find_bid(bid_id)
    tender = await find_tender(bid.tenderId)
    user = await is_user_responsible(username, tender.organizationId)
    await FeedbackDAO.add(
        tenderId=tender.id,
        bidFeedback=bid_feedback,
        creatorUsername=user.username,
        authorId=bid.authorId,
    )
    return bid


async def get_reviews(
    tender_id: UUID4,
    author_username: str,
    requester_username: str,
    limit: int,
    offset: int,
):
    """Получить ревью на предложения по фидбеку"""
    tender = await find_tender(tender_id)
    a_user = await find_user(username=author_username)
    await is_user_responsible(requester_username, tender.organizationId)
    reviews = await FeedbackDAO.find_all(
        limit, offset, authorId=a_user.id, tenderId=tender_id
    )
    return reviews
