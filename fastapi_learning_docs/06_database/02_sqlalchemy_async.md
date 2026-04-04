# FastAPI 数据库（二）异步访问关系库

在 async 路由里若仍用同步 SQLAlchemy Session，查询与提交会占用事件循环。异步方案让数据库 IO 与 await 配合，更适合高并发 API。

（上一篇：[SQLAlchemy 同步引擎](./01_sqlalchemy_sync.md)。）

---

## 一、常见两条路线

1. **databases（encode）**  
   轻量异步 SQL：手写 SQL 或 Core 表达式，不是完整 ORM。适合简单查询。

2. **SQLAlchemy 2.x 异步 ORM**  
   与同步版同一套 DeclarativeBase / select 模型，引擎换 create_async_engine，会话换 AsyncSession，操作用 await。团队已用 ORM 时优先这条。

驱动示例：PostgreSQL 用 asyncpg，MySQL 用 aiomysql，SQLite 用 aiosqlite。

---

## 二、安装（按需）

```bash
# encode databases + SQLite
pip install databases aiosqlite

# SQLAlchemy 异步 + SQLite
pip install sqlalchemy aiosqlite

# SQLAlchemy 异步 + PostgreSQL
pip install sqlalchemy asyncpg

# SQLAlchemy 异步 + MySQL
pip install sqlalchemy aiomysql
```

psycopg2-binary 是同步驱动，不能替代 asyncpg 做 SQLAlchemy asyncio 访问。

---

## 三、databases 极简用法

```python
from contextlib import asynccontextmanager

import databases
from fastapi import FastAPI

DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/users")
async def list_users():
    rows = await database.fetch_all("SELECT id, name FROM users")
    return [dict(r) for r in rows]
```

生命周期请用 lifespan，避免弃用的 on_event。

---

## 四、SQLAlchemy 异步 ORM

### 1. 引擎与会话工厂

使用 async_sessionmaker（不要再用 sessionmaker(..., class_=AsyncSession) 的旧拼法）：

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./demo.db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
```

MySQL：mysql+aiomysql://...  
PostgreSQL：postgresql+asyncpg://...

### 2. 异步 get_db

```python
from collections.abc import AsyncGenerator


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

### 3. 路由里查询

```python
from fastapi import Depends
from sqlalchemy import select


@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBUser))
    return list(result.scalars().all())
```

写操作：await db.commit()、await db.refresh(obj)。建表：

```python
async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
```

结束前可 await engine.dispose()（常放在 lifespan yield 之后）。

---

## 五、同步 vs 异步

| | 同步 | 异步 |
|--|------|------|
| 引擎 | create_engine | create_async_engine |
| 会话工厂 | sessionmaker | async_sessionmaker |
| get_db | def + yield + close | async def + async with + yield |
| 查询 | 同步 execute | await db.execute |
| 路由 | def 推荐 | async def |

bcrypt / passlib 仍是同步 CPU 工作，在 async 里直接调用会短暂阻塞；要求高可用 asyncio.to_thread 包一层。

---

## 一句话

异步 ORM：create_async_engine + async_sessionmaker + AsyncSession，查询提交一律 await；databases 适合轻量异步 SQL。

---

## 可运行示例

与同步篇同结构的注册 / 登录 / users/me，默认 sqlite+aiosqlite：

[`fastapi_db_async_sqlalchemy_demo.py`](./fastapi_db_async_sqlalchemy_demo.py)
