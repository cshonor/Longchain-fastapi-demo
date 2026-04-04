# CORS 跨域与 `CORSMiddleware`

**CORS（Cross-Origin Resource Sharing）** 是浏览器的安全机制：页面所在「源」与接口「源」在**协议 / 主机 / 端口**任一不同时即 **跨域**，默认会限制 JS 读取跨域响应；服务端需返回约定的 **CORS 响应头** 才能放行。

FastAPI 通过 Starlette 的 **`CORSMiddleware`**，用 **`app.add_middleware`** 统一加这些头。

（与 [内置中间件](./02_advanced_builtin_middleware.md) 同一注册方式。）

---

## 一、常用配置示例

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 二、核心参数（速查）

| 参数 | 含义 |
|------|------|
| `allow_origins` | 允许的源列表；**不要**与下面「凭证 + `*`」乱配（见下文） |
| `allow_origin_regex` | 用正则匹配允许的源 |
| `allow_methods` | 允许的方法；默认常见为 `["GET"]`，前后端分离常配 `["*"]` 或显式列表 |
| `allow_headers` | 允许的请求头 |
| `allow_credentials` | 是否允许携带 **Cookie、`Authorization` 等凭证** |
| `expose_headers` | 允许前端 JS 读取的**响应**头名 |
| `max_age` | **预检 OPTIONS** 结果缓存时间（秒） |

---

## 三、简单请求 vs 预检（Preflight）

**简单请求**（概念上）：方法多为 GET/HEAD/POST，且头与 `Content-Type` 受限；浏览器可直接发主请求，服务端响应里带 CORS 头即可。

**预检**：使用 PUT/DELETE、带 `Authorization`、或 `Content-Type: application/json` 等「非简单」场景时，浏览器往往先发 **`OPTIONS`**，通过后再发真实请求。`CORSMiddleware` 会处理这类预检。

---

## 四、开发便利 vs 生产安全

- **生产**：`allow_origins` 写**明确的前端域名**（含协议与端口），按需收紧 `allow_methods` / `allow_headers`。  
- **`allow_origins=["*"]`**：表示任意源；**浏览器规范不允许**在 **`allow_credentials=True`** 时同时使用 `*`（凭证场景下 `Access-Control-Allow-Origin` 不能是 `*`）。  
  - 需要 Cookie / Token 时：请列出**具体源**。  
  - 若坚持「全开」且不带凭证：可 `allow_origins=["*"]` 且 **`allow_credentials=False`**（仍要评估安全风险）。

---

## 一句话

**跨域是浏览器规则；`CORSMiddleware` 负责按配置自动补 CORS 响应头；带凭证时不要用 `*` 当来源。**

---

## 可运行示例

见 [`fastapi_cors_demo.py`](./fastapi_cors_demo.py)。
