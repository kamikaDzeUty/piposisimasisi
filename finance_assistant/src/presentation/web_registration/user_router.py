from typing import List
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.adapters.repositories.file_user_repository import FileUserRepository
from src.usecases.manage_tracked_symbols import (
    ListTrackedSymbolsUseCase,
    AddTrackedSymbolUseCase,
    RemoveTrackedSymbolUseCase,
)

router = APIRouter(prefix="/users", tags=["users"])

def get_user_repo():
    return FileUserRepository(Path("users.json"))

class SymbolRequest(BaseModel):
    symbol: str

@router.get(
    "/{username}/tracked",
    response_model=List[str],
    summary="Получить список отслеживаемых тикеров"
)
def list_tracked(
    username: str,
    repo: FileUserRepository = Depends(get_user_repo)
):
    uc = ListTrackedSymbolsUseCase(repo)
    try:
        return uc.execute(username)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post(
    "/{username}/tracked",
    response_model=List[str],
    status_code=status.HTTP_201_CREATED,
    summary="Добавить новый тикер в список"
)
def add_tracked(
    username: str,
    req: SymbolRequest,
    repo: FileUserRepository = Depends(get_user_repo)
):
    uc = AddTrackedSymbolUseCase(repo)
    try:
        return uc.execute(username, req.symbol.upper())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete(
    "/{username}/tracked/{symbol}",
    response_model=List[str],
    summary="Удалить тикер из списка"
)
def remove_tracked(
    username: str,
    symbol: str,
    repo: FileUserRepository = Depends(get_user_repo)
):
    uc = RemoveTrackedSymbolUseCase(repo)
    try:
        return uc.execute(username, symbol.upper())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
