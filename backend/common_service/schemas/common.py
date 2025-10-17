# item_service/schemas/item.py
from pydantic import BaseModel, Field
from typing import Optional


class ItemBase(BaseModel):
    """Базовая схема для элемента."""
    title: str = Field(..., min_length=1, max_length=255, description="Название элемента")
    description: Optional[str] = Field(None, max_length=1000, description="Описание элемента")


class ItemCreate(ItemBase):
    """Схема для создания элемента."""
    pass


class ItemUpdate(BaseModel):
    """Схема для обновления элемента."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Название элемента")
    description: Optional[str] = Field(None, max_length=1000, description="Описание элемента")


class ItemResponse(ItemBase):
    """Схема ответа для элемента."""
    id: int = Field(..., description="Уникальный идентификатор элемента")

    class Config:
        from_attributes = True
