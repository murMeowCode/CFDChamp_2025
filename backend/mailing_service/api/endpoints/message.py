"""апи для работы с сообщениями""" #pylint: disable=E0401
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from mailing_service.schemas.message import (
    MessageResponse,
    MessageListResponse
)
from mailing_service.services.message_service import MessageService
from shared.database.database import get_db

router = APIRouter(prefix="/mailing", tags=["mailing"])

@router.get("/users/{user_id}/messages", response_model=MessageListResponse)
async def get_user_messages(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Получение всех непрочитанных сообщений пользователя"""
    service = MessageService(db)
    messages = await service.get_user_messages(user_id)
    stats = await service.get_user_stats(user_id)

    return MessageListResponse(
        messages=messages,
        unread_count=stats["unread"]
    )

@router.patch("/users/{user_id}/messages/{message_id}/read", response_model=MessageResponse)
async def mark_message_as_read(
    user_id: str,
    message_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Пометить сообщение как прочитанное"""
    service = MessageService(db)
    message = await service.mark_as_read(message_id, user_id)

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    return message
