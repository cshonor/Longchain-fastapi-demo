"""
Path(...) 路径参数校验 + * 关键字形参示例，对应 11_path_params_path_core.md

运行：
  uvicorn fastapi_path_params_core_demo:app --reload --app-dir fastapi_learning_docs/02_fastapi_basics

文档：http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Path, Query

app = FastAPI(title="Path(...) core demo")


@app.get("/items/{item_id}")
async def read_items(item_id: int = Path(..., title="物品 ID", gt=0, le=1000)):
    return {"item_id": item_id}


# * 之后全是 keyword-only：Path(...) 与必填 Query 可一起写
@app.get("/items/{item_id}/detail")
async def read_items_detail(
    *,
    item_id: int = Path(..., gt=0),
    q: str,
    size: float = Query(1.0, gt=0, lt=10.5),
):
    return {"item_id": item_id, "q": q, "size": size}


@app.get("/")
def root():
    return {
        "docs": "/docs",
        "try": [
            "GET /items/1",
            "GET /items/0   # 422 (gt=0)",
            "GET /items/1/detail?q=hello",
            "GET /items/1/detail?q=hello&size=2.5",
        ],
    }
