"""Схемы для общего сервиса"""
from typing import Optional
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Базовая схема для элемента."""
    title: str = Field(..., min_length=1, max_length=255, description="Название элемента")
    description: Optional[str] = Field(None, max_length=1000, description="Описание элемента")


class ItemCreate(ItemBase):
    """Схема для создания элемента."""


class ItemUpdate(BaseModel):
    """Схема для обновления элемента."""
    title: Optional[str] = Field(None, min_length=1, max_length=255,
                                description="Название элемента")
    description: Optional[str] = Field(None, max_length=1000, description="Описание элемента")


class ItemResponse(ItemBase):
    """Схема ответа для элемента."""
    id: int = Field(..., description="Уникальный идентификатор элемента")

    class Config:
        """Класс для перехода в режим ORM"""
        from_attributes = True
