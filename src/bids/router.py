"""Эндпоинты роутера /bids"""
# pylint: disable=invalid-name

from typing import Literal

from fastapi import APIRouter
from pydantic import UUID4

from bids.schemas import BidsS, EditBidsS, FeedbackS, NewBidsS
from bids.service import (
    add_feedback,
    create_new_bid,
    edit_bid,
    edit_status_bid,
    find_tenders_bids,
    find_users_bids,
    get_reviews,
    get_status_bid,
    rollback_bid,
    submit_user_decision,
)

router = APIRouter(prefix="/bids")


@router.post("/new")
async def create_bid(bid: NewBidsS) -> BidsS:
    """Создание нового предложения"""
    return await create_new_bid(bid)


@router.get("/my")
async def get_users_bids(username: str, limit: int = 5, offset: int = 0) -> list[BidsS]:
    """Получение предложений отправленных пользователем"""
    return await find_users_bids(username, limit, offset)


@router.get("/{tenderId}/list")
async def get_tender_bids(
    tenderId: UUID4, username: str, limit: int = 5, offset: int = 0
):
    """Получение списка предложений на тендер"""
    return await find_tenders_bids(tenderId, username, limit, offset)


@router.get("/{bidId}/status")
async def get_bids_status(bidId: UUID4, username: str) -> str:
    """Получение статуса предложения"""
    return await get_status_bid(bidId, username)


@router.put("/{bidId}/status")
async def edit_bids_status(
    bidId: UUID4, status: Literal["Created", "Published", "Canceled"], username: str
) -> BidsS:
    """Изменение статуса предложения"""
    return await edit_status_bid(bidId, status, username)


@router.patch("/{bidId}/edit")
async def edit_bid_by_id(bidId: UUID4, username: str, data: EditBidsS) -> BidsS:
    """Изменение данных предложения"""
    return await edit_bid(bidId, username, dict(data))


@router.put("/{bidId}/submit_decision")
async def submit_decision(
    bidId: UUID4, decision: Literal["Approved", "Rejected"], username: str
) -> BidsS:
    """Отправка решения по предложению"""
    return await submit_user_decision(bidId, decision, username)


@router.put("/{bidId}/feedback")
async def add_feedback_bid(bidId: UUID4, bidFeedback: str, username: str) -> BidsS:
    """Отправка отзыва по предложению"""
    return await add_feedback(bidId, bidFeedback, username)


@router.put("/{bidId}/rollback/{version}")
async def rollback_bid_by_id(bidId: UUID4, version: int, username: str) -> BidsS:
    """Откат версии предложения"""
    return await rollback_bid(bidId, version, username)


@router.get("{tenderId}/reviews")
async def get_author_reviews(
    tenderId: UUID4,
    authorUsername: str,
    requesterUsername: str,
    limit: int = 5,
    offset: int = 0,
) -> list[FeedbackS]:
    """Просмотр отзывов на прошлые предложения"""
    return await get_reviews(tenderId, authorUsername, requesterUsername, limit, offset)
