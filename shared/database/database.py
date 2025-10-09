from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, Integer
from shared.config.base import settings
import logging

logger = logging.getLogger(__name__)

class PreBase:
    @declared_attr
    def __tablename__(cls):  # pylint: disable=E0213
        # Именем таблицы будет название модели в нижнем регистре.
        return cls.__name__.lower()  # pylint: disable=E1101
    # Во все таблицы будет добавлено поле ID.
    id = Column(Integer, primary_key=True)

class Base(PreBase):
    pass

# Создаем engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Для разработки, в продакшене False
    pool_size=5,
    max_overflow=10
)

# Создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db() -> AsyncSession:
    """Зависимость для получения сессии БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
