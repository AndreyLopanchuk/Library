from typing import Any, TypeVar

from sqlalchemy import select, func

from src.core.models.base_model import Base

DB = TypeVar("DB", bound=Base)


class FetcherRepository:
    """
    Класс для взаимодействия с базой данных. позволяет выполнять запросы для фильтрации и пагинации.

    Attributes:
        session (AsyncSession): Сессия SQLAlchemy для работы с базой данных.
    """

    def __init__(self, session):
        self.session = session

    async def get_total_count(self, model: DB, filter_dict: dict) -> int:
        """
        Получение количества объектов в базе данных с учётом фильтра.

        Args:
            model: Модель объекта.
            filter_dict: Словарь фильтрации.

        Returns:
            int: Количество объектов в базе данных с учётом фильтра.
        """
        if filter_dict:
            stmt = select(func.count(model.id)).filter_by(**filter_dict)
        else:
            stmt = select(func.count(model.id))

        return await self.session.scalar(stmt)

    async def get_obj_list(self, model: DB, offset: int, limit: int, filter_dict: dict) -> list[DB]:
        """
        Получение списка объектов с пагинацией и фильтрацией.

        Args:
            model: Модель объекта.
            filter_dict: Словарь фильтрации.
            offset: Начальный индекс пагинации.
            limit: Количество объектов для пагинации.

        Returns:
            List: Список объектов базы данных.
        """
        if filter_dict:
            stmt = select(model).filter_by(**filter_dict).order_by(model.id).offset(offset).limit(limit)
        else:
            stmt = select(model).order_by(model.id).offset(offset).limit(limit)
        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    def get_filter_dict(self, model: DB, field: str, value: Any) -> dict:
        """
        Создание словаря фильтрации.

        Args:
            model: Модель объекта.
            field: Имя поля для фильтрации.
            value: Значение для фильтрации.

        Returns:
            dict: Словарь c фильтром и значением.
        """
        if field and hasattr(model, field):
            convert_value = self.convert_value_to_field_type(model, field, value)
            return {field: convert_value}

        return dict()

    def convert_value_to_field_type(self, model: DB, field: str, value: Any) -> Any:
        """
        Преобразование значения к типу поля модели.

        Args:
            model: Модель объекта.
            field: Имя поля для фильтрации.
            value: Значение для фильтрации.

        Returns:
            Any: Преобразованное значение, если преобразование успешно, иначе None.
        """
        column = getattr(model, field)
        column_type = column.type
        try:
            converted_value = column_type.python_type(value)
            return converted_value

        except (ValueError, TypeError):
            return None
