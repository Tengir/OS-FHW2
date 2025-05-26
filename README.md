
| Вход | ─► | File-Store MS | ─► | File-Analysis MS | ─► | Выход |
|------|----|---------------|----|------------------|----|--------|
| .txt | →  | хранит .txt   | →  | считает абзацы/слова/символы, генерирует PNG-облако (QuickChart) | →  | JSON + PNG |

---

## 1. Состав

| Сервис           | Порт | Назначение                                          |
|------------------|------|-----------------------------------------------------|
| **api-gateway**  | 8000 | «Фасад»; просто проксирует запросы во внутренние MS |
| **file-store**   | 8001 | Загружает/выдаёт .txt, хранит метаданные в Postgres |
| **file-analysis**| 8002 | Считает статистику, берёт .txt из file-store, генерирует PNG |
| **db\_store**    | 5432 | Postgres 16 (таблица `files`)                       |
| **db\_analysis** | 5433 | Postgres 16 (таблица `stats`)                       |

> **Database-per-Service** – каждая бизнес-область имеет свою БД → независимые миграции, чёткие границы.

---

## 2. Реальная (чистая) архитектура в каждом сервисе

```

presentation  ← FastAPI routes / DI
└── application/use\_cases  ←  Interactor-ы («Сценарии»)
└── domain            ←  Entities + Ports (интерфейсы)
└── infrastructure ←  Adapters (SQLAlchemy, диск, HTTP Gateway)

```

Паттерны/приёмы 🔹
- **Hexagonal / Ports & Adapters** – FileStoreGatewayAdapter, DiskStorageAdapter …  
- **Repository** – `PostgresFileRepository`, `PostgresStatsRepository`
- **Use-case / Interactor** – один класс = один сценарий (`UploadFileInteractor`, `AnalyseFileInteractor`)
- **DTO / Cmd / Query** – чистые Pydantic-модели между слоями
- **Dependency Injection** через `Depends()` + `@lru_cache` (= ленивый singleton)
- **CQRS-лайт** – команды (`UploadFileCmd`) separados от чтения (`GetFileQuery`)
- **Idempotency** – SHA-256 check в `UploadFileInteractor` предотвращает дубли

---

## 3. Дерево каталогов (сверху корень repo)

```

.
├─ api-gateway/
│  └─ (FastAPI, routes, Dockerfile)
├─ file-store/
│  ├─ file\_store/
│  │  ├─ application/
│  │  ├─ domain/
│  │  ├─ infrastructure/
│  │  └─ presentation/
│  └─ Dockerfile
├─ file-analysis/
│  └─ (аналогичная структура)
├─ storage/
│  ├─ store/      ← том для .txt
│  └─ analysis/   ← том для PNG
├─ docker-compose.yml
└─ tests/         ← unit + e2e (pytest)

````

---

## 4. Public API (via API-Gateway :8000)

| Метод + URL                     | Тело / параметры              | Ответ | Описание |
|---------------------------------|------------------------------|-------|-----------|
| `POST /upload`                  | multipart-form `file`        | `201 {id}` | Загрузить .txt |
| `GET /files/{uuid}`             | –                            | raw .txt | Скачать текст |
| `GET /analyze/{uuid}`           | –                            | JSON  | Статистика + путь к PNG |
| `GET /cloud/{path}`             | –                            | image/png | PNG-облако |

❌ ошибки:

| Статус | Когда |
|--------|-------|
| `404`  | файл/PNG отсутствует |
| `415`  | неверный `Content-Type` в upload |
| `422`  | плохой UUID / пустой multipart |

Полная коллекция для Postman лежит в ​`/docs/file_analysis_postman_collection.json`.

---

## 5. Запуск & тесты

```bash
# 1. собрать и стартануть
docker compose build
docker compose up
````

## 6. Переменные окружения

| Переменная                 | По умолчанию                       | Где используется             |
| -------------------------- | ---------------------------------- | ---------------------------- |
| `FILE_DB_DSN`              | `postgresql+asyncpg://…/store`     | file-store                   |
| `FILE_STORAGE_ROOT`        | `/app/storage` (volume)            | file-store / DiskStorage     |
| `DB_DSN`                   | `postgresql+psycopg2://…/analysis` | file-analysis                |
| `STORAGE_ROOT`             | `/app/storage`                     | file-analysis / DiskStorage  |
| `FILE_STORE_URL`           | `http://file-store:8001`           | file-analysis (HTTP Gateway) |
| `ANALYSIS_URL`             | `http://file-analysis:8002`        | api-gateway                  |
| `MAX_CONN`, `HTTP_TIMEOUT` | 50 / 5 сек                         | httpx client limits          |

---

## 7. Как это работает (коротко)

1. **Загрузка**: API-Gateway при `POST /upload` проксирует файл → File-Store.
2. File-Store вычисляет SHA-256, если дубликат — отдаёт старый UUID, иначе:

   * кладёт .txt на диск
   * сохраняет метаданные в `db_store.files`
3. **Анализ**: API-Gateway вызывает File-Analysis:

   1. File-Analysis через `FileStoreGatewayAdapter` тянет оригинальный .txt
   2. Считает абзацы/слова/символы
   3. Отправляет текст в QuickChart (GET `/wordcloud`) → получает PNG
   4. PNG кладётся на диск, статистика — в `db_analysis.stats`
4. **Скачивание**: любые `.txt` и `.png` отдаются напрямую.

---

## 8. Проверка на крайние случаи

Готовые Postman-запросы включают:

| Тест                                   | Ожидание           |
| -------------------------------------- | ------------------ |
| upload 0-байтового файла               | 201, stats = 0-0-0 |
| повторный upload того же контента      | один и тот же UUID |
| download/analysis несуществующего UUID | 404                |
| download PNG по фейковому пути         | 404                |
| upload без поля `file`                 | 422                |

(см. коллекцию).

---

## 9. Коллекция postman и скрины лежат в репозитории
