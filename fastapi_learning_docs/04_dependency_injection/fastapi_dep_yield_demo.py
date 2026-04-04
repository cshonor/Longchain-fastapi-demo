"""
yield 依赖（请求后收尾）— 对应 05_di_yield_dependencies.md

运行：
  uvicorn fastapi_dep_yield_demo:app --reload --app-dir fastapi_learning_docs/04_dependency_injection

文档：http://127.0.0.1:8000/docs

GET /stats/ 可看到累计 close 次数；每访问一次 /items/ 或 /items-cm/ 应各 +1。
"""

import uuid

from fastapi import Depends, FastAPI

app = FastAPI(title="Yield dependency demo")

_close_count = 0


class FakeDBSession:
    """模拟 ORM Session：仅记录 id 与是否已 close。"""

    def __init__(self, label: str) -> None:
        self.label = label
        self.closed = False

    def close(self) -> None:
        global _close_count
        if not self.closed:
            self.closed = True
            _close_count += 1


async def get_db():
    db = FakeDBSession(f"try-finally-{uuid.uuid4().hex[:8]}")
    try:
        yield db
    finally:
        db.close()


class DbContext:
    """同步上下文管理器：对应笔记中的 MySuperContextManager 写法。"""

    def __init__(self) -> None:
        self.db = FakeDBSession(f"cm-{uuid.uuid4().hex[:8]}")

    def __enter__(self) -> FakeDBSession:
        return self.db

    def __exit__(self, exc_type, exc_val, tb) -> None:
        self.db.close()


async def get_db_via_cm():
    with DbContext() as db:
        yield db


@app.get("/items/")
async def read_items(db: FakeDBSession = Depends(get_db)):
    return {"session": db.label, "closed_in_handler": db.closed}


@app.get("/items-cm/")
async def read_items_cm(db: FakeDBSession = Depends(get_db_via_cm)):
    return {"session": db.label, "closed_in_handler": db.closed}


@app.get("/stats/")
def stats():
    return {"sessions_closed_total": _close_count}


@app.get("/")
def root():
    return {
        "docs": "/docs",
        "try": ["/items/", "/items-cm/", "/stats/"],
    }
