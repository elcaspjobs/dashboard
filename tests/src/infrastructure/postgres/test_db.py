import pytest
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import text


@pytest.mark.asyncio
async def test_db_connection(engine: AsyncEngine):
    """Проверяем, что соединение с БД работает."""
    async with engine.connect() as conn:
        # Выполняем простой SQL-запрос (например, проверка версии PostgreSQL)
        result = await conn.execute(text("SELECT 1"))
        value = result.scalar()
        assert value == 1, "Не удалось выполнить запрос к БД"
