from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

# 运行：
#   uvicorn demo:app --reload
# 访问：
#   http://127.0.0.1:8000/docs

app = FastAPI(title="FastAPI + Pydantic Demo")


# 请求体模型：FastAPI 会用 Pydantic 自动校验类型
class User(BaseModel):
    id: int  # 必传、必须是 int
    name: str = "jack guo"  # 可选（有默认值）
    signup_timestamp: datetime | None = None
    friends: list[int] = []


# 最基础的 GET 接口
@app.get("/")
def read_root():
    return {"Hello": "World"}


# 路径参数 + 查询参数（会自动做类型校验）
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


# POST + 请求体校验：传错字段/类型会自动返回 422
@app.post("/users")
def create_user(user: User):
    return user


# async 路由示例：当内部需要 await（例如异步 IO）时使用 async def
@app.get("/async")
async def read_async():
    return {"mode": "async", "ok": True}

from fastapi import FastAPI

# 创建 FastAPI 应用实例：启动后可访问 /docs（Swagger UI）
app = FastAPI(title="FastAPI Demo")


# 最基础的 GET 接口
@app.get("/")
def read_root():
    return {"Hello": "World"}


# 路径参数 item_id（会按 int 做类型校验）；q 是可选查询参数
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


# async 路由示例：当内部需要 await（例如异步 IO）时使用 async def
@app.get("/async")
async def read_async():
    return {"mode": "async", "ok": True}

