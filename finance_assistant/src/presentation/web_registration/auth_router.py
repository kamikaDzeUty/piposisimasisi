from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from pathlib import Path

from src.usecases.register_user import RegisterUserUseCase
from src.adapters.repositories.file_user_repository import FileUserRepository

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    password: str
    password2: str
    email: EmailStr

class RegisterResponse(BaseModel):
    message: str

def get_user_repo() -> FileUserRepository:
    return FileUserRepository(Path("users.json"))

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    req: RegisterRequest,
    repo: FileUserRepository = Depends(get_user_repo)
):
    uc = RegisterUserUseCase(repo)
    try:
        uc.execute(req.username, req.password, req.password2, req.email)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "User registered successfully"}
