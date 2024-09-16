"""Модуль для работы  с таблицами предложений и отзывов"""
# pylint: disable=too-few-public-methods

from sqlalchemy import and_, select

from bids.models import Bids, Feedback, VersionBids
from dao.base import BaseDAO
from database import async_session_maker
from tenders.dao import TendersDAO


class BidsDAO(TendersDAO, BaseDAO):
    """Класс для работы с таблицой bids"""

    model = Bids

    @classmethod
    async def find_all(cls, limit, offset, **filter_by):
        """Получить все предложения последних версий, с фильтром"""
        filter_by = {k: v for k, v in filter_by.items() if v is not None}
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__)
                .filter_by(**filter_by)
                .join(
                    VersionBids,
                    and_(
                        cls.model.version == VersionBids.version,
                        cls.model.id == VersionBids.id,
                    ),
                )
                .order_by(cls.model.name)
                .offset(offset)
                .limit(limit)
            )
            result = await session.execute(query)
        return result.mappings().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """Поиск предложения по filter_by (версии и id)"""
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__)
                .filter_by(**filter_by)
                .join(
                    VersionBids,
                    and_(
                        cls.model.version == VersionBids.version,
                        cls.model.id == VersionBids.id,
                    ),
                    isouter=True,
                )
            )
            result = await session.execute(query)
            return result.mappings().one_or_none()


class VersionBidsDAO(BaseDAO):
    """Класс для работы с таблицой version_bids"""

    model = VersionBids


class FeedbackDAO(BaseDAO):
    """Класс для работы с таблицой feedback"""

    model = Feedback

    @classmethod
    async def find_all(cls, limit, offset, **filter_by):
        """Поиск всех отзывов по фильтру filter_by"""
        filter_by = {k: v for k, v in filter_by.items() if v is not None}
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__.columns)
                .filter_by(**filter_by)
                .offset(offset)
                .limit(limit)
            )
            result = await session.execute(query)
            return result.mappings().all()
