"""апи для работы с элементами"""#pylint: disable=E0401, E0611
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from shared.database.database import get_db
from shared.utils.auth_utils import get_auth_dependency
from common_service.schemas.common import ItemResponse, ItemCreate, ItemUpdate
from common_service.models.common import Item

router = APIRouter()

@router.get("/items", response_model=List[ItemResponse])
async def get_all_items(
    db: Session = Depends(get_db),
    user: dict = Depends(get_auth_dependency().get_current_user)
):
    """Получение всех элементов (только для аутентифицированных пользователей)"""
    items = db.query(Item).all()
    return items

@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_auth_dependency().get_current_user)
):
    """Получение элемента по ID (только для аутентифицированных пользователей)"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: ItemCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_auth_dependency().get_current_user)
):
    """Создание нового элемента (только для аутентифицированных пользователей)"""
    new_item = Item(
        title=item_data.title,
        description=item_data.description
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_data: ItemUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_auth_dependency().get_current_user)
):
    """Обновление элемента по ID (только для аутентифицированных пользователей)"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Обновление полей, если они предоставлены
    if item_data.title is not None:
        item.title = item_data.title
    if item_data.description is not None:
        item.description = item_data.description
    
    db.commit()
    db.refresh(item)
    return item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_auth_dependency().get_current_user)
):
    """Удаление элемента по ID (только для аутентифицированных пользователей)"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return None