"""служба работы с сообщениями""" #pylint: disable=E0401,E1102
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from mailing_service.models.message import Message


class MessageService:
    """класс службы"""
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_messages(
        self,
        user_id: str,
    ) -> List[Message]:
        """Получение сообщений пользователя с фильтрацией"""
        stmt = select(Message).where(Message.user_id == user_id)

        stmt = stmt.where(Message.is_read is False)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_message_by_id(self, message_id: str, user_id: str) -> Optional[Message]:
        """Получение конкретного сообщения по ID"""
        stmt = select(Message).where(
            Message.id == message_id,
            Message.user_id == user_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def mark_as_read(self, message_id: str, user_id: str) -> Optional[Message]:
        """Пометить сообщение как прочитанное"""
        message = await self.get_message_by_id(message_id, user_id)
        if message and not message.is_read:
            message.is_read = True
            await self.db.commit()
            await self.db.refresh(message)
        return message
