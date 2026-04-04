"""
OAuth2 密码流 + JWT 签发 — 对应 02_oauth2_jwt_token.md

依赖：PyJWT、python-multipart（见仓库 requirements.txt）

运行：
  uvicorn fastapi_security_oauth2_jwt_token_demo:app --reload --app-dir fastapi_learning_docs/05_security

文档：http://127.0.0.1:8000/docs
  在 /token 使用 OAuth2PasswordRequestForm：username、password（任意非空即可通过本 demo）
"""

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

# 仅本地学习用；生产环境必须用环境变量或密钥管理服务
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="OAuth2 + JWT token demo")


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta is not None else timedelta(minutes=15)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 真实项目：查库、校验密码哈希；此处任意用户名密码均签发 Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
def root():
    return {
        "docs": "/docs",
        "token": "POST /token (form: username, password)",
    }
