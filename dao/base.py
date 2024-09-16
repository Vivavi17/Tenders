"""Модуль для работы с BaseDAO"""

from sqlalchemy import insert, select, update

from database import async_session_maker


class BaseDAO:
    """Родительский класс для работы с БД"""

    model = None

    @classmethod
    async def find_all(cls, limit, offset, **filter_by):
        """Поиск всех записей с фильтром и пагинацией"""
        filter_by = {k: v for k, v in filter_by.items() if v is not None}
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__.columns)
                .filter_by(**filter_by)
                .order_by(cls.model.name)
                .offset(offset)
                .limit(limit)
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """Поиск одной записи"""
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def add(cls, **data):
        """Добавление записи в таблицу"""
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @classmethod
    async def update(cls, object_id, **data):
        """Обновление данных записи по ID"""
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == object_id)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar()
