"""схемы для работы с сообщениями"""
from typing import List, Optional
from pydantic import BaseModel

# Base schemas
class MessageBase(BaseModel):
    """базовый класс сообщения"""
    subject: str
    content: str
    user_id: str

class MessageUpdate(BaseModel):
    """схема обновления статуса сообщения"""
    is_read: Optional[bool] = None

# Response schemas
class MessageResponse(BaseModel):
    """схема ответа"""
    id: str
    user_id: str
    subject: str
    content: str
    is_read: bool

    class Config:
        """класс для перехода в ORM"""
        from_attributes = True

class MessageListResponse(BaseModel):
    """список сообщений"""
    messages: List[MessageResponse]
    unread_count: int

class StatusResponse(BaseModel):
    """ответ на изменение статуса"""
    status: str
    message: str
