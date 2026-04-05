# LangChain 核心：`PromptTemplate` 与 `ChatPromptTemplate`

## 一、核心定义

**`PromptTemplate` / `ChatPromptTemplate` 用来把「模板」和「变量」拆开**：固定文案里留 `{占位符}`，运行时再 `format` / `invoke` 填入。  
前者面向**单段字符串**；后者面向**对话消息列表**（system / human / ai 等），与 **ChatModel** 配套。

（与 [LLM / ChatModel](./04_llm_chatmodel_usage.md) 对照：补全模型多用 `PromptTemplate`；对话模型多用 `ChatPromptTemplate`。）

---

## 二、为什么要用模板？

1. **维护性**：提示集中在一处，改模板即可，少复制粘贴。  
2. **多变量**：比零散 f-string 更易读；复杂场景可再拆子模板。  
3. **接链（LCEL）**：`prompt | llm | ...` 与 Runnable 协议一致，便于组合与测试。

---

## 三、两种常用类型

### 1. `PromptTemplate`（单段文本）

适合单次任务：摘要、起名、分类等。

```python
from langchain_core.prompts import PromptTemplate

template = "给生产 {product} 的公司取一个好听的名字。"
prompt = PromptTemplate.from_template(template)
final_prompt = prompt.format(product="保温杯")
print(final_prompt)
# 给生产 保温杯 的公司取一个好听的名字。
```

### 2. `ChatPromptTemplate`（多角色消息）

适合多轮、人设、与 **ChatModel** 对接。

```python
from langchain_core.prompts import ChatPromptTemplate

system_template = "你是一个专业的 {role}，只回答 {language} 问题。"
human_template = "{question}"

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("human", human_template),
    ]
)

final_messages = chat_prompt.format_messages(
    role="Python 工程师",
    language="中文",
    question="如何高效学习 Python？",
)
# list[BaseMessage]，如 SystemMessage + HumanMessage
```

---

## 四、链式调用（LCEL）

**类型要对齐**：`ChatPromptTemplate` 输出消息列表，应接 **ChatModel**；`PromptTemplate` 输出字符串，应接 **LLM（补全）**。

### 示例 A：`ChatPromptTemplate | ChatModel`

```python
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个助手，围绕 {topic} 帮助用户。"),
        ("human", "{content}"),
    ]
)
llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.environ["DEEPSEEK_API_KEY"],
)

chain = prompt | llm
result = chain.invoke(
    {"topic": "创意生成", "content": "给杯子公司起 3 个名字"}
)
# result 一般为 AIMessage，文本在 result.content
```

### 示例 B：`PromptTemplate | LLM（补全）`

```python
import os

from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "你是起名助手。产品：{product}。请给出 3 个公司名，逗号分隔。"
)
llm = Tongyi(api_key=os.environ["DASHSCOPE_API_KEY"])
chain = prompt | llm
text = chain.invoke({"product": "保温杯"})
```

---

## 五、f-string 与模板对比（直观）

```python
product = "保温杯"

# f-string：提示与业务混在同一处，复用和测试都费劲
s1 = f"给生产 {product} 的公司取一个好听的名字。"

# PromptTemplate：模板可单测、可入库、可接链
from langchain_core.prompts import PromptTemplate

p = PromptTemplate.from_template("给生产 {product} 的公司取一个好听的名字。")
s2 = p.format(product=product)
```

---

## 六、一句话

**Prompt 模板 = 把提示词结构化、参数化**；不改变模型本身能力，但让应用更好维护、更好接 **LCEL**。

---

## 延伸阅读

- [基础链三要素 & 模块](./02_basic_chain_and_modules.md)  
- [环境搭建 & 核心概念](./01_env_and_core_concepts.md)
