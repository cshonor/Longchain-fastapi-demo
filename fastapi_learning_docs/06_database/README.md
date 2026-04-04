# 06 — 数据库访问（Database access）

**核心内容**：SQLAlchemy 2.0 模型与 Session；同步与异步访问选型。  
**核心目标**：可靠持久化与迁移流程（生产可配合 Alembic）。

对照代码：`fastapi_app/db/session.py`、`fastapi_app/db/models/`。

---

## 本章笔记

- [SQLAlchemy 同步引擎（Session、模型与 JWT 骨架）](./01_sqlalchemy_sync.md)
- [异步访问关系库（databases / SQLAlchemy asyncio）](./02_sqlalchemy_async.md)
- [同步数据库 Demo（SQLite，可换 MySQL）](./fastapi_db_sync_sqlalchemy_demo.py)
- [异步 SQLAlchemy Demo（aiosqlite + JWT）](./fastapi_db_async_sqlalchemy_demo.py)
