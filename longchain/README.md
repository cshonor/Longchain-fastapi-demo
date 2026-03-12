# Longchain 模块

存放 LangChain 相关逻辑。

## 职责

- LLM 模型配置与初始化
- 提示词（Prompts）模板
- 链（Chains）定义
- 工具（Tools）与代理（Agents）
- 向量存储、文档加载器等 RAG 组件

## 典型结构

```
longchain/
├── chains/        # 链定义
├── prompts/       # 提示词模板
├── models/        # 模型配置
└── tools/         # 自定义工具
```
