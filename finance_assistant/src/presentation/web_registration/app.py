from fastapi import FastAPI
from src.presentation.web_registration.auth_router import router as auth_router
from src.presentation.web_registration.user_router import router as user_router

app = FastAPI(title="Finance Assistant API", version="0.1")

# Роуты регистрации
app.include_router(auth_router, prefix="/auth", tags=["auth"])
# Роуты управления tracked_symbols
app.include_router(user_router)  