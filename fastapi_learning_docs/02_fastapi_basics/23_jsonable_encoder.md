# jsonable_encoder 用法

fastapi.encoders.jsonable_encoder 把 Pydantic 模型、datetime、set、Decimal 等不能直接被 json.dumps 的值，转成 dict、list、str、int、float、bool、None 组成的结构。

用途：手写 JSONResponse 前生成 content；json.dumps、缓存、日志、下游只认 JSON 的场景。

与 [直接返回 Response / JSONResponse](./19_direct_return_response.md) 配合阅读。

## 示例

```python
from datetime import datetime
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):
    return jsonable_encoder(item)
```

请求体 timestamp 建议 ISO 8601，例如 2017-11-23T16:10:10（带 T 更易被 Pydantic 解析）。

## 常见规则

Pydantic 模型转 dict 再递归；datetime、date 常变 ISO 字符串；set 变 list；Decimal 常变 float；None 保留。嵌套 dict、list 递归。

Pydantic v2 若只做模型导出也可用 model_dump(mode="json")；与 FastAPI 手写 JSONResponse 时 jsonable_encoder 习惯一致。

## 可运行示例

[`fastapi_jsonable_encoder_demo.py`](./fastapi_jsonable_encoder_demo.py)
