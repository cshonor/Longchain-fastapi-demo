from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field

# 运行：
#   uvicorn fastapi_learning_docs.02_fastapi_basics.demo:app --reload
# 文档：
#   http://127.0.0.1:8000/docs

app = FastAPI(title="FastAPI + Pydantic Demo")


# 请求体模型：FastAPI 会用 Pydantic 自动校验类型
class User(BaseModel):
    id: int  # 必传、必须是 int
    name: str = "jack guo"  # 可选（有默认值）
    signup_timestamp: datetime | None = None # 可选（有默认值） | None 表示可以为空
    friends: list[int] = []


# 响应模型示例：用于 response_model（限制/规范输出字段）
class UserPublic(BaseModel):
    id: int
    name: str


class ItemOut(BaseModel):
    item_id: int
    q: str | None = None
    note: str = Field(default="typed path + query params")


# 最基础的 GET 接口
@app.get("/")
def read_root():
    return {"Hello": "World"}


# 路径参数 + 查询参数（会自动做类型校验）
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


# 例子 1：路径参数类型校验
# - 正确：/path/123
# - 错误：/path/abc  -> 422
@app.get("/path/{item_id}")
def path_param_example(item_id: int):
    return {"item_id": item_id}


# 例子 2：查询参数类型校验
# - 正确：/query?limit=10&debug=true
# - 错误：/query?limit=abc -> 422
@app.get("/query")
def query_param_example(limit: int = 10, debug: bool = False):
    return {"limit": limit, "debug": debug}


# POST + 请求体校验：传错字段/类型会自动返回 422
@app.post("/users")
def create_user(user: User):
    return user


# 例子 3：请求体 JSON 格式与字段类型校验（Body）
# 在 /docs 里 POST /users/validate，传错类型会直接 422
@app.post("/users/validate")
def validate_body_example(user: User):
    return {"ok": True, "user": user}


# 例子 4：响应格式约束（response_model）
# 即使内部返回了多余字段，也会被 response_model 过滤成规范输出
@app.get("/users/{user_id}", response_model=UserPublic)
def response_model_example(user_id: int):
    return {
        "id": user_id,
        "name": "jack guo",
        "friends": [1, 2, 3],  # 会被过滤掉（不在 UserPublic 里）
    }


# 同样的 response_model 示例：同时约束路径参数和查询参数的返回结构
@app.get("/items_out/{item_id}", response_model=ItemOut)
def response_model_item_example(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q, "extra": "will be removed"}


# async 路由示例：当内部需要 await（例如异步 IO）时使用 async def
@app.get("/async")
async def read_async():
    return {"mode": "async", "ok": True}

