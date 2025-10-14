"""служба работы с сообщениями""" #pylint: disable=E0401,E1102
import logging
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from mailing_service.models.message import Message

logger = logging.getLogger(__name__)

class MessageService:
    """класс службы"""
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(self, user_id: str, subject: str, content: str) -> Message:
        """Создание нового сообщения"""
        message = Message(
            user_id=user_id,
            subject=subject,
            content=content,
            is_read=False  # По умолчанию непрочитанное
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_user_messages(
        self,
        user_id: str,
    ) -> List[Message]:
        """Получение сообщений пользователя с фильтрацией"""
        logger.info(
            "🟡 Начало получения сообщений пользователя",
            extra={
                "user_id": user_id,
                "service": "MessageService",
                "method": "get_user_messages"
            }
        )
        
        try:
            # Логируем формирование запроса
            logger.debug(
                "🔍 Формирование SQL запроса для получения сообщений",
                extra={
                    "user_id": user_id,
                    "filter_read": False  # Только непрочитанные
                }
            )
            
            # ВАЖНО: Исправляем условие - было неверно
            stmt = select(Message).where(
                Message.user_id == user_id,
                Message.is_read == False  # Правильное условие
            )

            # Логируем сформированный запрос
            logger.debug(
                "📝 Сформированный SQL запрос",
                extra={
                    "query": str(stmt),
                    "parameters": {"user_id": user_id}
                }
            )

            # Выполняем запрос к БД
            logger.info("⚡ Выполнение запроса к базе данных")
            
            result = await self.db.execute(stmt)
            messages = result.scalars().all()
            

            # Логируем результаты запроса
            logger.info(
                "✅ Успешно получены сообщения из базы данных",
                extra={
                    "user_id": user_id,
                    "messages_count": len(messages),
                    "message_ids": [str(msg.id) for msg in messages] if messages else []
                }
            )

            if not messages:
                logger.warning(
                    "⚠️ Сообщения не найдены для пользователя",
                    extra={
                        "user_id": user_id,
                        "filter_applied": "only_unread"
                    }
                )
            else:
                logger.debug(
                    "📨 Детали найденных сообщений",
                    extra={
                        "user_id": user_id,
                        "messages_details": [
                            {
                                "message_id": str(msg.id),
                                "title": getattr(msg, 'title', 'N/A'),
                                "is_read": getattr(msg, 'is_read', 'N/A'),
                                "created_at": getattr(msg, 'created_at', 'N/A')
                            } for msg in messages
                        ]
                    }
                )

            return messages

        except Exception as e:
            logger.error(
                "❌ Ошибка при получении сообщений пользователя",
                extra={
                    "user_id": user_id,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "service": "MessageService"
                },
                exc_info=True
            )
            raise

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
