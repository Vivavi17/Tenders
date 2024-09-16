"""Модуль для работы с запросами к существующими таблицами БД"""

from sqlalchemy import select

from dao.base import BaseDAO
from database import async_session_maker
from models import Employee, Organization, OrganizationResponsible


class EmployeeDAO(BaseDAO): # pylint: disable=too-few-public-methods
    """Класс для запросов в таблицу employee"""

    model = Employee


class OrganizationDAO(BaseDAO): # pylint: disable=too-few-public-methods
    """Класс для запросов в таблицу organization"""

    model = Organization


class OrganizationResponsibleDAO(BaseDAO): # pylint: disable=too-few-public-methods
    """Класс для запросов в таблицу organization_responsible"""

    model = OrganizationResponsible

    @classmethod
    async def find_all(cls, **filter_by):
        """Вывод всех пользователей после фильтрации по filter_by"""
        filter_by = {k: v for k, v in filter_by.items() if v is not None}
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
