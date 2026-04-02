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

# 运行：
#   uvicorn fastapi_learning_docs.02_fastapi_basics.fastapi_hello_demo:app --reload
#
# 访问：
#   http://127.0.0.1:8000/
#   http://127.0.0.1:8000/items/5?q=test
#   http://127.0.0.1:8000/async
#   http://127.0.0.1:8000/docs