# MVP Каталог Ресторанов и Кафе

Это асинхронный бэкенд на Python для каталога ресторанов и кафе, построенный на базе FastAPI, SQLAlchemy 2.0+ (asyncio + asyncpg) и PostgreSQL.

В будущем приложение будет интегрировано с Telegram Mini App, а на текущем этапе представляет собой чистое JSON API.

## 🛠 Технологический стек

- **Язык**: Python 3.11+ (контейнер использует Python 3.12)
- **Веб-фреймворк**: [FastAPI](https://fastapi.tiangolo.com/)
- **Валидация данных**: [Pydantic v2](https://docs.pydantic.dev/)
- **ORM**: [SQLAlchemy 2.0+](https://docs.sqlalchemy.org/) (асинхронный режим `asyncio` + драйвер `asyncpg`)
- **База данных**: PostgreSQL 16 (с заделом на расширение PostGIS)
- **Контейнеризация**: Docker & Docker Compose

---

## 📁 Структура проекта

Логика приложения разделена на слои в соответствии с лучшими практиками проектирования многослойных (N-Tier) архитектур:

```text
RestaurantsCatalog/
├── app/
│   ├── __init__.py
│   ├── main.py             # Точка входа в FastAPI, инициализация приложения, жизненный цикл (lifespan)
│   ├── database.py         # Настройка асинхронного подключения к БД (Engine, SessionMaker, Base)
│   ├── models.py           # Декларативные SQLAlchemy 2.0+ модели (Entity Layer)
│   ├── schemas.py          # Валидационные схемы Pydantic v2 (DTO / Presentation Layer)
│   └── routers/
│       ├── __init__.py
│       └── restaurants.py  # Эндпоинты для работы с заведениями (API Layer)
├── Dockerfile              # Контейнеризация FastAPI приложения
├── docker-compose.yml      # Оркестрация контейнеров FastAPI и PostgreSQL (с healthcheck для DB)
├── pyproject.toml          # Зависимости и метаданные проекта (PEP 621 + build-system)
├── main.py                 # Локальная точка запуска (для IDE / ручного запуска без Docker)
└── README.md               # Документация проекта
```

---

## 🚀 Как запустить проект

Убедитесь, что у вас установлены [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).

### 1. Запуск в Docker (Рекомендуемый способ)

Выполните команду в корневой директории проекта:

```bash
docker compose up --build
```

**Что произойдет автоматически при старте:**
1. Поднимется контейнер `restaurants_db` с СУБД PostgreSQL.
2. Сработает `healthcheck` базы данных, проверяя готовность принимать соединения.
3. Поднимется контейнер `restaurants_web` с FastAPI.
4. FastAPI-приложение автоматически применит схемы и создаст таблицу `restaurants` в БД.
5. Приложение проверит базу данных на наличие записей. Если БД пуста, сработает **автоматический сидинг (seeding)** и в базу будут добавлены 4 демонстрационных ресторана разных кухонь.
6. Веб-сервер запустится на порту `8000` в режиме горячей перезагрузки (при изменении кода файлы в контейнере обновятся автоматически).

---

## 🔌 Использование API

После успешного запуска приложение доступно по адресу: http://localhost:8000

- **Интерактивная документация Swagger UI**: http://localhost:8000/docs
- **Альтернативная документация ReDoc**: http://localhost:8000/redoc

### Основные эндпоинты

#### 1. Главная страница (Root)
- **URL**: `GET /`
- **Описание**: Проверка работоспособности сервиса и ссылки на документацию.

#### 2. Получение списка ресторанов с фильтрацией
- **URL**: `GET /api/restaurants`
- **Параметры запроса (Query Params)**:
  - `cuisine_type` (string, optional): Фильтрация по типу кухни (регистронезависимая, поиск по подстроке). Например: `Italian`, `Japanese`, `American`.
  - `min_rating` (float, optional): Фильтрация по минимальному рейтингу (от 0.0 до 5.0).
- **Пример ответа (JSON)**:
  ```json
  [
    {
      "name": "La Trattoria",
      "location": "123 Italian Way, Moscow",
      "price_level": 2,
      "open_time": "11:00:00",
      "close_time": "23:00:00",
      "cuisine_type": "Italian",
      "restaurant_type": "Casual",
      "rating": 4.5,
      "id": 1
    }
  ]
  ```

##### Примеры запросов с фильтрацией:
- Только итальянская кухня: http://localhost:8000/api/restaurants?cuisine_type=italian
- Рестораны с рейтингом не ниже 4.6: http://localhost:8000/api/restaurants?min_rating=4.6
- Комбинированный фильтр: http://localhost:8000/api/restaurants?cuisine_type=japanese&min_rating=4.5

---

## 💡 Дополнительные детали реализации

1. **Асинхронность**: Весь цикл обработки запросов — от веб-сервера до получения данных из СУБД — полностью асинхронный (используются `async/await`, `create_async_engine`, `async_sessionmaker`, `AsyncSession` и асинхронный драйвер базы данных `asyncpg`).
2. **Безопасная очередность запуска (Compose)**: Благодаря блоку `depends_on` с условием `condition: service_healthy` для БД, FastAPI-приложение запускается только после полной инициализации PostgreSQL. Это исключает падения на старте.
3. **Pydantic v2**: Используется современная конфигурация `model_config = ConfigDict(from_attributes=True)` для удобного преобразования SQLAlchemy-моделей в DTO.
4. **Разделение слоев (N-Tier)**: Логика работы с БД отделена от схем валидации и маршрутов. Это гарантирует масштабируемость: в будущем легко добавить слой сервисов (`services.py`) и репозиториев (`repositories.py`) для более сложных бизнес-операций.
