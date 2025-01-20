from typing import Any


class PaginatedFetcher:
    """
    Класс для получения пагинированного списка объектов с учетом фильтрации.

    Attributes:
        repository (FetcherRepository): Экземпляр репозитория для взаимодействия с базой данных.
        offset (int): Начальный индекс для пагинации.
        limit (int): Количество объектов для пагинации.
        field (str): Поле для фильтрации.
        value (Any): Значение для фильтрации.

    """

    def __init__(self, repository, offset: int, limit: int, field: str | None, value: Any | None):
        self.repository = repository
        self.offset = offset
        self.limit = limit
        self.field = field
        self.value = value

    async def get_paginated_list(self, model, extra_filters: dict = None) -> dict:
        """
        Получение отфильтрованного и пагинированного списка объектов.

        Args:
            model (DB): Модель объекта.
            extra_filters (dict): Дополнительные фильтры.

        Returns:
            dict: Словарь с данными пагинации:
                - offset: Начальный индекс.
                - limit: Количество объектов.
                - totalCount: Общее количество объектов с учетом фильтра.
                - data: Список объектов.

        """
        filter_dict = self.repository.get_filter_dict(model=model, field=self.field, value=self.value)
        if extra_filters:
            filter_dict.update(extra_filters)
        pagination = {
            "offset": self.offset,
            "limit": self.limit,
            "totalCount": await self.repository.get_total_count(model=model, filter_dict=filter_dict),
            "data": await self.repository.get_obj_list(
                model=model, offset=self.offset, limit=self.limit, filter_dict=filter_dict
            ),
        }

        return pagination

    async def fetch_by_reader_id(self, model, reader_id: int) -> dict:
        """
        Получение отфильтрованного и пагинированного списка объектов по идентификатору пользователя.

        Args:
            model: Модель объекта.
            reader_id (int): Идентификатор пользователя.

        Returns:
            dict: Словарь с фильтром по id пользователя.
        """
        extra_filters = {"reader_id": reader_id}
        return await self.get_paginated_list(model=model, extra_filters=extra_filters)
