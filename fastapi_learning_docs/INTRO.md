# FastAPI 学习笔记简介（从这里开始）

这套笔记的目标是：**用最短路径把 FastAPI 写到“能上线”的水平**（不仅是能跑 demo 路由）。

你会同时使用两部分：

- **学习文档**：`fastapi_learning_docs/`（按模块拆分的笔记与示例）
- **可运行代码**：`fastapi_app/`（项目骨架，用于对照实践）

---

## 推荐学习顺序

1. **异步基础**：`01_python_coroutines/`（`await`、EventLoop、Task / Future）
2. **写接口与校验**：`02_fastapi_basics/`（路由、参数、Body、Pydantic、`/docs`）
3. **骨架工程化**：`03_response_middleware/` + `04_dependency_injection/`
4. **上生产核心**：`05_security/` + `06_database/`
5. **进阶补齐**：`07_advanced/`

完整路线与周期建议见：[LEARNING_GUIDE.md](./LEARNING_GUIDE.md)。

---

## 快速入口

- 总索引：[README.md](./README.md)
- 学习路线：[LEARNING_GUIDE.md](./LEARNING_GUIDE.md)

# FastAPI 学习笔记简介（从这里开始）

这套笔记的目标是：**用最短路径把 FastAPI 写到“能上线”的水平**（不是只会写几个 demo 路由）。

你会同时使用两部分：

- **学习文档**：`fastapi_learning_docs/`（按模块拆分的笔记与示例）
- **可运行代码**：`fastapi_app/`（项目骨架，用于对照实践）

---

## 你应该怎么学（推荐节奏）

1. **先学异步**：从 `01_python_coroutines/` 开始，搞懂 `await`、EventLoop、Task/Future。
2. **再写接口**：进 `02_fastapi_basics/`，把路由、参数、Body、Pydantic 校验写熟。
3. **工程化骨架**：`03_response_middleware/` + `04_dependency_injection/`，把响应、中间件、依赖注入体系搭起来。
4. **上生产核心**：`05_security/`（JWT/OAuth2）+ `06_database/`（SQLAlchemy 2.0）。
5. **补齐进阶**：`07_advanced/`（异常、后台任务、生命周期等）。

完整路线与周期建议见：[LEARNING_GUIDE.md](./LEARNING_GUIDE.md)。

---

## 你会得到什么（学习产出）

- **会写**：清晰的路由拆分、稳定的请求/响应模型、可复用依赖
- **会改**：能在不推翻代码的情况下扩展认证、数据库、日志与异常体系
- **会排错**：遇到 422、依赖注入、事件循环相关问题能快速定位

---

## 快速入口

- 路线总览：[LEARNING_GUIDE.md](./LEARNING_GUIDE.md)
- 模块目录索引：[README.md](./README.md)

