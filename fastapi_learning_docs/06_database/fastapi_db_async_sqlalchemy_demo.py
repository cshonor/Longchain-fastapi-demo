"""
SQLAlchemy 异步 ORM + SQLite（aiosqlite）— 对应 02_sqlalchemy_async.md

依赖：sqlalchemy、aiosqlite、PyJWT、python-multipart、passlib[bcrypt]

MySQL 示例：DATABASE_URL = "mysql+aiomysql://user:pass@host:3306/db" 并安装 aiomysql

运行：
  uvicorn fastapi_db_async_sqlalchemy_demo:app --reload --app-dir fastapi_learning_docs/06_database

文档：http://127.0.0.1:8000/docs
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./demo_async.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class DBUser(Base):
    __tablename__ = "test_user"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(100), unique=True, index=True)
    password = mapped_column(String(255))
    sex = mapped_column(String(10), nullable=True)
    login_time = mapped_column(Integer, nullable=True)
    create_date = mapped_column(DateTime(timezone=True), nullable=True)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    sex: str | None = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="SQLAlchemy async DB demo", lifespan=lifespan)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_user_by_username(db: AsyncSession, username: str) -> DBUser | None:
    r = await db.execute(select(DBUser).where(DBUser.username == username))
    return r.scalar_one_or_none()


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> DBUser | None:
    user = await get_user_by_username(db, username)
    if user is None:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta is not None else timedelta(minutes=15)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="无效的认证凭据",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> DBUser:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or not isinstance(username, str):
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = await get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/register", response_model=User)
async def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    if await get_user_by_username(db, form_data.username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    now = datetime.now(timezone.utc)
    db_user = DBUser(
        username=form_data.username,
        password=get_password_hash(form_data.password),
        sex=None,
        login_time=None,
        create_date=now,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@app.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.username}, expires_delta=delta)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_me(current_user: DBUser = Depends(get_current_user)):
    return current_user


@app.get("/")
async def root():
    return {
        "docs": "/docs",
        "db_url_hint": "默认 sqlite+aiosqlite；可改为 mysql+aiomysql://...",
        "flow": ["POST /register", "POST /login", "GET /users/me"],
    }
