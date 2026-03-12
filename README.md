# Longchain-FastAPI

基于 LangChain 与 FastAPI 的 LLM 应用 API 项目。

## 项目结构

```
longchain/
├── longchain/     # LangChain 相关逻辑（链、提示、模型等）
├── fastapi/       # FastAPI 路由、接口与中间件
└── README.md
```

## 技术栈

- **LangChain** - 大语言模型应用开发框架
- **FastAPI** - 高性能 Python Web 框架

## 环境要求

- Python 3.8+
- pip

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/cshonor/Longchain-fastapi.git
cd Longchain-fastapi
```

### 2. 创建虚拟环境

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行服务

```bash
uvicorn main:app --reload
```

## 配置

在项目根目录创建 `.env` 文件，配置必要的环境变量（如 API Keys）。

## License

MIT
