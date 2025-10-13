"""основной модуль сервиса""" #pylint: disable=E0401
from fastapi import FastAPI
from mailing_service.api.endpoints.message import router as mailing_router

app = FastAPI(title="CFDChamp API")

app.include_router(mailing_router)

@app.get("/health")
async def health_check():
    """апи для проверки работоспособности сервиса"""
    return {"status": "healthy", "service": "auth_service"}
