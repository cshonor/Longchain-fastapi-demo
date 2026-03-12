# FastAPI 模块

存放 FastAPI 路由、接口与中间件。

## 职责

- API 路由定义
- 请求/响应模型（Pydantic）
- 中间件（跨域、日志、认证等）
- 依赖注入
- WebSocket 接口（如需流式输出）

## 典型结构

```
fastapi/
├── routes/        # API 路由
├── models/        # Pydantic 模型
├── middleware/    # 中间件
└── dependencies/  # 依赖注入
```
