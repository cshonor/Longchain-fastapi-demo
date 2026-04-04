# FastAPI 安全机制（一）简介

FastAPI 把「谁可以访问接口」放在 **OpenAPI** 同一套模型里描述，并在 **`fastapi.security`** 里提供常用构造器，减少手写协议细节。本章后续会落到具体写法（Bearer、OAuth2 密码流、JWT 等）；本篇先对齐**常见协议**与 **OpenAPI 安全方案类型**。

（前置：[依赖注入](../04_dependency_injection/01_di_introduction.md) 常用于把校验逻辑注入路由。）

---

## 一、常见安全相关协议

### 1. OAuth2

- **认证与授权**框架：由授权服务器签发访问凭证，资源服务器按策略放行。  
- 常见形态包括**第三方登录**（微信、QQ、GitHub 等）与各类 **access token** 流程。

### 2. OpenID Connect（OIDC）

- 在 **OAuth2** 之上扩展，标准化 **ID Token** 与用户信息端点。  
- 许多「用 Google / 企业账号登录」的方案基于 OIDC。

### 3. OpenAPI 中的安全方案（Security Schemes）

OpenAPI 3.x 定义了若干 **security scheme** 类型，FastAPI 生成的文档与 `/docs` 会按声明展示「如何带凭证调用接口」。常见四类：

| 类型 | 含义 |
|------|------|
| **apiKey** | 密钥出现在 **Query**、**Header** 或 **Cookie** |
| **http** | **HTTP Basic**、**Digest**、**Bearer**（如 JWT 常挂在 Bearer 里） |
| **oauth2** | OAuth2 各授权流（implicit、password、clientCredentials、authorizationCode 等） |
| **openIdConnect** | OpenID Connect 发现（**OpenID Connect Discovery**） |

实际项目里还会配合 **HTTPS**、**CORS**、**限流**、**依赖注入里的校验**等，共同构成完整安全边界。

---

## 二、FastAPI 中的实现入口

- 模块 **`fastapi.security`**：如 `APIKeyHeader`、`HTTPBearer`、`OAuth2PasswordBearer`、`OAuth2AuthorizationCodeBearer` 等，用于声明依赖、生成 OpenAPI 安全定义并与请求解析对齐。  
- 具体路由上通常 **`Depends(...)`** 取凭证、验签或换用户信息，失败则 **`HTTPException`**。

---

## 一句话

**FastAPI 按 OpenAPI 标准描述安全方案，并内置工具支持 apiKey、HTTP 认证、OAuth2、OpenID Connect 等常见模式。**
