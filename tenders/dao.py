"""Модуль для работы с запросами к таблицам тендеров"""

from sqlalchemy import and_, select, update

from dao.base import BaseDAO
from database import async_session_maker
from tenders.models import Tenders, VersionTenders


class TendersDAO(BaseDAO):
    """Запросы в таблицу tenders"""

    model = Tenders

    @classmethod
    async def find_all(cls, limit, offset, **filter_by):
        """Получение последних версий тендеров с фильтрацией и пагинацией"""
        filter_by = {k: v for k, v in filter_by.items() if v is not None}
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__)
                .filter_by(**filter_by)
                .join(
                    VersionTenders,
                    and_(
                        cls.model.version == VersionTenders.version,
                        cls.model.id == VersionTenders.id,
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
        """Поиск тендера последней версии по фильтру"""
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__)
                .filter_by(**filter_by)
                .join(
                    VersionTenders,
                    and_(
                        cls.model.version == VersionTenders.version,
                        cls.model.id == VersionTenders.id,
                    ),
                    isouter=True,
                )
            )
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def update_status(cls, object_id, version, **data):
        """Обновить статус тендера"""
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(and_(cls.model.id == object_id, cls.model.version == version))
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @classmethod
    async def update(cls, pk, **data):
        """Обновить данные тендера по pk"""
        data = {k: v for k, v in data.items() if v is not None}
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.pk == pk)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar()


class VersionTendersDAO(BaseDAO):# pylint: disable=too-few-public-methods
    """Класс для работы с таблицей version_tenders"""
    model = VersionTenders

    @classmethod
    async def update(cls, tender_id, **data):
        """Обновление созраненной версии тендера"""
        data = {k: v for k, v in data.items() if v is not None}
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == tender_id)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar()
