# Longchain-FastAPI

基于 **LangChain** 与 **FastAPI** 的 LLM 应用 API 与学习笔记仓库。

## 项目结构

```
longchain/
├── fastapi_app/            # FastAPI 可运行应用（入口见 fastapi_app/main.py）
├── fastapi_learning_docs/  # FastAPI 系统化学习文档（含 01～08 章，见该目录 README）
├── longchain/              # LangChain 相关工具与 env 示例（含 env.example）
├── langchain-learning-notes/  # LangChain 学习笔记（可选）
├── demo.py                 # 本地实验脚本
├── environment.yml         # Conda 环境
├── requirements.txt        # pip 依赖
└── README.md
```

## 技术栈

- **LangChain** — LLM 应用编排
- **FastAPI** — Web API（异步、OpenAPI）

## 环境要求

- **Python 3.10+**（与 LangChain / 当前依赖一致即可）
- 推荐使用 **Anaconda**，亦可用 **venv + pip**

## 快速开始（Conda）

```bash
git clone https://github.com/cshonor/Longchain-fastapi.git
cd Longchain-fastapi
conda env create -f environment.yml
conda activate longchain-fastapi
```

### 运行 API

```bash
uvicorn fastapi_app.main:app --reload
```

默认接口前缀：`/api/v1`；文档：`http://127.0.0.1:8000/docs`。

### 更新 Conda 环境

```bash
conda env update -f environment.yml
```

## 使用 pip + venv

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
uvicorn fastapi_app.main:app --reload
```

## 配置

在项目**根目录**创建 `.env`。可复制模板：

```bash
copy longchain\env.example .env   # Windows
# cp longchain/env.example .env   # Linux / macOS
```

按需填写各 LLM / 服务 API Key；应用通过 `pydantic-settings` 读取根目录 `.env`（见 `fastapi_app/core/config.py`）。

## 学习文档

系统化的 FastAPI 笔记与可运行小 demo 在 **`fastapi_learning_docs/`**，总索引：[fastapi_learning_docs/README.md](fastapi_learning_docs/README.md)（协程 → 基础 → 中间件 → 依赖注入 → 安全 → 数据库 → 进阶 → **测试**）。

## License

MIT
