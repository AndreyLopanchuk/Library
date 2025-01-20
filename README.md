# API для управления библиотекой

## Архитектура приложения
## app: отвечает за основную логику приложения.
- #### api:  
Содержит все API-маршруты, связанные с книгами, авторами и выдачами книг.   
Требуемый сервис получает через Depends зависимость.
- #### services: 
AuthorService(AuthorRepository), BookService(BookRepository) и BorrowService(BorrowRepository).   
При необходимости через конструктор класса сервис получает другой сервис необходимы ему для обработки запроса.  
- #### repository:  
репозитории книг, авторов и выдач, связанные с базой данных.  
- #### models:   
модели Author, Book и Borrow, связанные с базой данных.  
## auth: проверка подлинности пользователей, управление доступом и другие функции, связанные с безопасностью.
- #### api: 
API-маршруты, для аутентификациеи, авторизации и управления пользователями.  
- #### services:  
AuthService(AuthRepository), PasswordManager, JWTokenManager(TokenRepository).
- #### repository:  
AuthRepository и TokenRepository.
## core: содержит базовые классы и функции, используемые в других модулях.
- ### database:
Управление сессиями базы данных, подключение к базе данных и другие функции, связанные с базой данных.
PostgreSQL и Redis
- ### services: 
BaseService и PaginatedFetcher(PaginatedFetcherRepository)  
- #### repository: 
BaseRepository и PaginatedFetcherRepository(Репозиторий отвечающий за фильтрацию и пагинацию)
- #### models:  
Базовая модель базы данных и модель User
- #### errors
Содержит ошибки с app, repository и services
- #### config
файл конфигурации
- #### log_config
Настройки логирования. Логи пишутся для всех событий изменения базы данных в app (create, update, delete)

## Контейнеризация:
Приложение, PostgreSQL, Redis запускаются в разных Docker контейнерах. 
Тесты и тестовые базы данных так же запускаются в разных Docker контейнерах.
Сетевое взаимодействия между микросервисами осуществляется через Docker Network.

## Установка и Запуск
склонируте репозиторий:  
```sh
git clone https://github.com/AndreyLopanchuk/Library.git
```  
Для запуска веб-приложения введите команду в корне проекта:  
```sh
docker-compose up --build
```
Пробросы томов на локальную машину закоментированы в docker-compose.yml
PostgreSQL, Redis и логирование сохраняют данные только в контейнере.

## Тестирование
Для запуска тестов введите команду из папки tests:
```sh
docker-compose up --build -d && docker-compose logs -f testapp
```

## Документация
Реализована встроенная FastAP OpenAPI документация.  

ссылка на задание:  
https://docs.google.com/document/d/1ej6Qdhf65VP6d8rPCti2wdiD680p91UKu6GQS7i-IKs/edit?hl=ru&tab=t.0

### Технологический стек
- PostgreSql - Основная база данных
- Redis - База данных для хранения refresh токенов
- Fastapi - фреймворк для разработки RESTful API
- Uvicorn - сервер для запуска FastAPI-приложения
- Pydantic - библиотека для работы с данными и валидации
- Sqlalchemy - библиотека для работы с базой данных
- Pytest - фреймворк для написания и запуска тестов
- Docker - контейнеризация приложения, БД и тестов
- JWT - библиотека для работы с токенами
- bcrypt - библиотека для хеширования паролей
