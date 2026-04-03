# FastAPI Path：路径参数与校验（速记）

路径参数写在 URL 的 `{xxx}` 里。需要**元信息、校验、文档**时用 **`Path(...)`**（与 `Query(...)` 用法高度相似）。  
（与 [路径参数八句话](./02_path_params_8_sentences.md)、[路径 + Query 混用](./10_path_and_query_mix.md) 一起看。）

---

## 1. 基本用法

- 从 `fastapi` 导入 **`Path`**，专门修饰**路径参数**。
- 路径参数在路由里是**必出现**的；在 `Path(...)` 里用 **`...`** 表示必填（与 `Query(...)` 一致）。

```python
from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(item_id: int = Path(..., title="物品 ID")):
    return {"item_id": item_id}
```

---

## 2. 参数顺序与 `*`（关键字-only）

Python 规则：**没有默认值的形参**一般要写在**有默认值**的形参前面，否则会语法错误。

在 FastAPI 里：

Path(...)：即使写 Path(...)（省略默认值），Python 仍视为 “有默认值”（因为 Path 是函数调用）。

必填 Query：不写默认值（如 q: str），属于 “无默认值、必填”。
直接写会报 Python 语法错：

```python
# ❌ 错误：有默认值的 Path 放在了必填 Query 前面
@app.get("/items/{item_id}")
def read_item(item_id: int = Path(...), q: str):  # SyntaxError
    ...

```    

路由里常见组合是：**路径参数常带 `Path(...)`（算“有默认值”）**，后面还要接**必填的 Query** 时，容易纠结顺序。

可以用 **`*` 分隔符**：`*` 之后的参数全部是**仅限关键字**，便于把「路径 + 查询」写清楚。在函数参数里加一个单独的 *，* 之后所有参数强制变成「关键字参数」，Python 不再检查顺序。

```python
@app.get("/items/{item_id}")
async def read_items(
     *,  # 👈 关键分隔符
    item_id: int = Path(..., title="商品ID", ge=1),  # 路径参数（必填）
    q: str,  # 查询参数（必填，无默认值）
    limit: int = Query(10, le=100)  # 查询参数（可选）
):
    return {"item_id": item_id, "q": q, "limit": limit}
```

这里 `q: str` 表示**必填的查询参数**（未出现在路径 `{...}` 中 → Query）。

---

## 3. 数字校验（`int` / `float`，Path 与 Query 通用）

- `gt`：严格大于  
- `ge`：大于等于  
- `lt`：严格小于  
- `le`：小于等于  

示例：

```python
item_id: int = Path(..., gt=0, le=1000)
size: float = Query(..., gt=0, lt=10.5)
```

---

## 4. Path 与 Query 的区别（记位置）

| 修饰器 | 对应 URL 位置 | 典型形态 |
|--------|----------------|----------|
| `Path(...)` | 路径段 | `/items/{item_id}` |
| `Query(...)` | 查询串 | `/items?q=xxx` |

校验字段（`gt/ge/lt/le`、`title`/`description`、`alias`、`deprecated` 等）在两者上的**直觉一致**：都是给「某一种来源的参数」加约束与文档。

---

## 一句话

**路径里用 `Path`，`?` 后面用 `Query`；要写复杂组合时用 `*` 把关键字参数理顺，数字范围用 `gt/ge/lt/le`。**

只要出现：Path(...) + 必填 Query
一律用 * 分隔，写成：

def 函数(*, path参数=Path(...), 必选Query, 可选Query=...)
