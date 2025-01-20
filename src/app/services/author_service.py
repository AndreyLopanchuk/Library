from src.app.models.author_model import Author
from src.app.repository.author_repository import AuthorRepository
from src.app.schemas.author_schema import AuthorCreate, AuthorUpdate
from src.core.services.base_service import BaseService


class AuthorService(BaseService):
    """
    Сервис для работы с авторами.

    Attributes:
        repository (AuthorRepository): Репозиторий для работы с авторами.
    """

    def __init__(self, author_repository: AuthorRepository):
        super().__init__(repository=author_repository)
