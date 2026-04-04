"""
CORSMiddleware 示例 — 对应 03_cors_middleware.md

运行：
  uvicorn fastapi_cors_demo:app --reload --app-dir fastapi_learning_docs/03_response_middleware

文档：http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CORS demo")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
def hello():
    return {"message": "ok"}


@app.get("/")
def root():
    return {
        "docs": "/docs",
        "cors_origins": origins,
        "note": "Browser page must be served from one of allow_origins to see CORS in action",
    }
