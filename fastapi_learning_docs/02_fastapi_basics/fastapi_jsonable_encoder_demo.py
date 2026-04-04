"""
jsonable_encoder — 对应 23_jsonable_encoder.md

运行：
  uvicorn fastapi_jsonable_encoder_demo:app --reload --app-dir fastapi_learning_docs/02_fastapi_basics

PUT /items/{item_id}，Body JSON 示例见笔记（timestamp 请用 ISO，如 2017-11-23T16:10:10）。
"""

from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI(title="jsonable_encoder demo")


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return {"item_id": item_id, "encoded": json_compatible_item_data}


@app.get("/")
def root():
    return {
        "docs": "/docs",
        "try_put": "PUT /items/foo with body title, timestamp (ISO), description",
    }
