"""апи для работы с сообщениями""" #pylint: disable=E0401, W0718
import asyncio
import json
import logging
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession
from mailing_service.schemas.message import (
    MessageResponse,
    MessageListResponse
)
from mailing_service.services.message_service import MessageService
from shared.utils.auth_utils import get_auth_dependency
from shared.database.database import get_db

router = APIRouter(prefix="/mailing", tags=["mailing"])
logger = logging.getLogger(__name__)

CHECK_INTERVAL = 2

@router.websocket("/ws/me/messages")
async def websocket_get_my_messages(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_auth_dependency().get_current_user_websocket)
):
    """WebSocket endpoint для получения непрочитанных сообщений с регулярной проверкой"""
    await websocket.accept()

    user_id = str(user["user_id"])
    service = MessageService(db)

    try:
        while True:
            try:
                # Получаем текущие непрочитанные сообщения
                messages = await service.get_user_messages(user_id)

                if messages:
                    response = MessageListResponse(
                        messages=messages,
                        unread_count=len(messages)
                    )
                    await websocket.send_text(response.json())
                else:
                    # Отправляем пустой ответ, если сообщений нет
                    empty_response = MessageListResponse(messages=[], unread_count=0)
                    await websocket.send_text(empty_response.json())

                # Ждем перед следующей проверкой
                await asyncio.sleep(CHECK_INTERVAL)

            except Exception as e:
                logger.error(
                    "❌ Ошибка в WebSocket соединении",
                    extra={
                        "user_id": user_id,
                        "error_type": type(e).__name__,
                        "error_message": str(e)
                    }
                )
                # Отправляем ошибку клиенту
                error_response = {
                    "type": "error",
                    "detail": "Произошла ошибка при получении сообщений"
                }
                await websocket.send_text(json.dumps(error_response))
                await asyncio.sleep(CHECK_INTERVAL)  # Ждем перед повторной попыткой

    except WebSocketDisconnect:
        logger.info(
            "🔌 WebSocket соединение закрыто",
            extra={"user_id": user_id}
        )
    except Exception as e:
        logger.error(
            "❌ Критическая ошибка в WebSocket",
            extra={
                "user_id": user_id,
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        )
        await websocket.close()

@router.patch("/me/messages/{message_id}/read", response_model=MessageResponse)
async def mark_my_message_as_read(
    message_id: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_auth_dependency().get_current_user)
):
    """Пометить сообщение текущего пользователя как прочитанное"""
    service = MessageService(db)
    message = await service.mark_as_read(message_id, str(user["user_id"]))

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    return message
