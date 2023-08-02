[![Python](https://img.shields.io/badge/python-%3E%3D3-blue)](https://www.python.org/downloads/release/python-311/)
[![Asyncio](https://img.shields.io/badge/asyncio-supported-green)](https://docs.python.org/3/library/asyncio.html)
[![FastAPI](https://img.shields.io/badge/fastapi-%3E%3D-red)](https://fastapi.tiangolo.com/)
[![SQLAlchemy version](https://img.shields.io/badge/sqlalchemy-%3E%3D2.0.16-yellow)](https://www.sqlalchemy.org/)
[![Alembic version](https://img.shields.io/badge/alembic-%3E%3D1.11.1-green)](https://alembic.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/postgres-supported-blue)](https://www.postgresql.org/)

# Проект Shift

Shift - это проект, предоставляющий API для управления пользователями в системе. Он позволяет создавать, обновлять, получать и удалять информацию о пользователях. Основная задача проекта - отображать информацию о зарплате сотрудника и дате ее повышения.

# Важно!

**Создавать, удалять пользователей и обновновлять информацию о них может только администратор.** После этого он выдают id и пароль для каждого сотрудника.

## Возможности

- Аутентификация пользователей с использованием токенов доступа
- Создание, обновление, получение и удаление пользователей
- Управление доступом на основе ролей с привилегиями администратора
- Интеграция с базой данных PostgreSQL

## Установка

**Для удобства использования можно использовать команды из `Makefile`**

1. Клонируйте репозиторий: `git clone https://github.com/your-user/shift.git`

2. Перейдите в каталог проекта: `cd shift`

3. Установите необходимые зависимости с помощью Poetry: `poetry install`

4. Настройте базу данных:

- Запустите сервер базы данных PostgreSQL командами `alembic init` и `alembic upgrade heads`
- Создайте новую базу данных и обновите настройки базы данных в файле `shift/settings.py`.

5. Запустите приложение: `poetry run uvicorn shift.main:app --reload`

6. Откройте приложение в веб-браузере по адресу `http://localhost:8000`.

## Использование

- Для аутентификации отправьте POST-запрос на `/login/` с идентификатором пользователя и паролем в теле запроса. Ответ будет содержать токен доступа.
- Используйте токен доступа в заголовке `Authorization` для последующих запросов, требующих аутентификации.
- Для создания, получения, обновления и удаления информации о пользователях используйте конечные точки API.
- **Созданы Docker контейнеры для самого проекта, базы данных и тестовой базы данных**

7. Доступные эндпоинты:

- Post-запрос на /user/create/ - создает нового пользователя 
- GET-запрос на /user/{user_id}/ - позволяет самому пользователю или админу получит информацию о пользователе
- PATCH-запрос на /user/{user_id}/ - позволяет админу изменить информацию о пользователе
- DELETE-запрос на /user/{user_id}/ -  позволяет админу удалить информацию о пользователе

## Документация

Подробную документацию по конечным точкам API и их использованию смотрите в "http://localhost:8000/docs", предоставляемой FastAPI.
