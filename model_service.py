"""Бизнес-логика работы с существующими таблицами"""

from exceptions import (
    OrganizationDoesntExistException,
    UserDoesntExistsException,
    UserDoesntHaveRightsException,
)
from model_dao import EmployeeDAO, OrganizationDAO, OrganizationResponsibleDAO


async def find_organization(**data: dict):
    """Поиск организации по параметрам data"""
    if not data:
        raise OrganizationDoesntExistException
    organization = await OrganizationDAO.find_one_or_none(**data)
    if not organization:
        raise OrganizationDoesntExistException
    return organization


async def find_user(**data: dict):
    """Поиск пользователя по параметрам data"""
    if not data:
        raise UserDoesntExistsException
    user = await EmployeeDAO.find_one_or_none(**data)
    if not user:
        raise UserDoesntExistsException
    return user


async def is_user_responsible(username: str, organization_id: str):
    """Поиск пользователя по username, проверка ответственности за организацию organization_id"""
    user = await find_user(username=username)
    is_responsible = await OrganizationResponsibleDAO.find_one_or_none(
        user_id=user.id, organization_id=organization_id
    )
    if not is_responsible:
        raise UserDoesntHaveRightsException
    return user


async def is_user_in_organization(**data: dict):
    """Поиск пользователя по data, проверка, находится ли пользователь в организации"""
    user = await find_user(**data)
    is_responsible = await OrganizationResponsibleDAO.find_one_or_none(user_id=user.id)
    if not is_responsible:
        raise UserDoesntHaveRightsException
    return user


async def count_responsible_user(organization_id: str) -> int:
    """Подсчет пользователей ответственных за организацию"""
    count = await OrganizationResponsibleDAO.find_all(organization_id=organization_id)
    return len(count)
