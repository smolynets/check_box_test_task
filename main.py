import os
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import tempfile

from database import SessionLocal, engine, get_db, Base
from auth import (
    get_password_hash,
    get_user,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from users.routers import router as users_router
from payments.routers import router as payments_router
import config


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=f"{config.SERVICE_NAME} API",
    description=f"API for the {config.SERVICE_NAME} project",
    debug=config.DEBUG
)


app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(payments_router, prefix="/payments", tags=["payments"])

# remove temp file for /payment/{receipt_link} endpoint
temporary_files = []

@app.on_event("shutdown")
async def cleanup():
    for tmp_file_path in temporary_files:
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
    temporary_files.clear()
