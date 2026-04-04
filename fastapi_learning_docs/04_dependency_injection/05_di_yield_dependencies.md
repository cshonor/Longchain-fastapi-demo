# FastAPI 依赖注入（五）yield 依赖项

**yield 依赖**：依赖函数用 **`yield`** 把资源交给路由；FastAPI 在**响应发送完成后**再继续执行 `yield` 之后的代码（通常配合 **`try` / `finally`** 做释放）。适合「每个请求一份资源、用完必收尾」的场景，典型是**数据库会话**。

（上一篇：[路径装饰器依赖](./04_di_path_decorator_dependencies.md)）

---

## 一、作用

在**请求处理完并返回响应之后**，再跑一段**收尾逻辑**，常见于：

- 关闭数据库连接或归还连接池
- 释放文件句柄、锁等
- 统一清理、补充日志

---

## 二、核心语法

用 **`yield`** 代替 **`return`**：

- **`yield` 之前**：请求进入路由前执行（创建、打开资源）。
- **`yield` 的值**：注入给路由参数。
- **`yield` 之后**：响应已发出后再执行（清理）；建议放在 **`finally`** 里，保证一定会执行。

```python
async def get_db():
    db = DBSession()    # 前置
    try:
        yield db        # 注入给路由
    finally:
        db.close()      # 后置：尽量保证总会执行
```

---

## 三、重要规则

1. **`yield` 之后不要再 `raise HTTPException`**  
   响应往往已经交给客户端，此时再抛 API 层异常，**无法**再变成正常的 HTTP 错误响应；应记录日志或做内部告警，需要时用普通 `Exception` 由服务器或中间件处理（仍可能表现为 500）。

2. **释放逻辑放在 `finally`（或等价的上下文管理器 `__exit__`）**，避免路由里提前 `return` 或异常时泄漏资源。

3. FastAPI 会把这种「先生成器、再收尾」的依赖**按异步上下文管理协议**接入请求生命周期（概念上可理解为：注入段与退出段）。

---

## 四、类上下文管理器版本

已有同步 **`with`** 封装时，可以在依赖里包一层再 `yield`：

```python
class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc, tb):
        self.db.close()


async def get_db():
    with MySuperContextManager() as db:
        yield db
```

异步资源优先用 **`async with`** 与具体库提供的异步上下文管理器；思路仍是：进入时拿到对象，注入，退出时释放。

---

## 一句话

**yield 依赖** = **请求前准备 + 把资源注入路由 + 响应后再收尾**，最适合按请求划分的连接与资源管理。

---

## 可运行示例

见 [`fastapi_dep_yield_demo.py`](./fastapi_dep_yield_demo.py)（用假 Session 演示关闭次数，无需真实数据库）。
