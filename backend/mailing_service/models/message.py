"""модели сообщений"""#pylint: disable=E0401,E1123
import uuid
from sqlalchemy import Column, String, Boolean, Text
from shared.database.database import Base

class Message(Base):
    """модель сообщения"""
    __tablename__ = "messages"

    id = Column(uuid.UUID(as_uuid=True), primary_key=True)
    user_id = Column(uuid.UUID(as_uuid=True), nullable=False, index=True)
    subject = Column(String(255), nullable=False)  # Тема письма
    content = Column(Text, nullable=False)  # Текст письма
    is_read = Column(Boolean, default=False)  # Статус прочтения

    def to_dict(self):
        """перевод модели в словарь"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "subject": self.subject,
            "content": self.content,
            "is_read": self.is_read
        }
