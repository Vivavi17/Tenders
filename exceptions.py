"""Модуль кастомных ошибок сервиса"""

from fastapi import HTTPException, status


class TendersException(HTTPException):
    """Базовый класс ошибок"""

    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserDoesntExistsException(TendersException):
    """Ошибка поиска пользователя"""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не существует или некорректен."


class OrganizationDoesntExistException(TendersException):
    """Ошибка поиска организации"""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Организация не существует или некорректна."


class BidDoesntExistException(TendersException):
    """Ошибка поиска предложения"""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Предложение не существует или некорректно."


class UserDoesntHaveRightsException(TendersException):
    """Ошибка прав пользователя"""

    status_code = status.HTTP_403_FORBIDDEN
    detail = "Недостаточно прав для выполнения действия."


class TenderDoesntExistException(TendersException):
    """Ошибка поиска тендера"""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Не найден тендер или его версия."
