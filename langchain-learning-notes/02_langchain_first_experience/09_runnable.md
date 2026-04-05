# 什么是 Python / LangChain 里的 **Runnable**？

与 [LCEL 组件组合](./07_lcel.md) 直接相关：**`|` 能串起来的前提，是每一段都是 `Runnable`（或兼容同一 Runnable 协议）**。

---

## 1. 最核心一句话（建议背下来）

**Runnable 是 LangChain 里「可执行组件」的统一标准接口。**  
只要一个对象遵循这套接口，它就能用 **`.invoke()`**（以及按需使用 **`.stream()`**、**`.batch()`** 等），也能被 **`|`** 拼进 LCEL 链里，和前后环节对接输入输出。

---

## 2. 大白话

把 **Runnable** 想成：**大家都按同一套规矩「能跑、能接、能组合」**。

不管你是：

- `PromptTemplate` / `ChatPromptTemplate`
- 补全 **LLM**（如 Tongyi）
- 对话 **ChatModel**（如 ChatDeepSeek）
- **OutputParser**
- 还是用 **`|`** 拼出来的**整条链**

只要走 Runnable 这套约定，你就可以：

- **单次调用**：`invoke`
- **流式**：`stream`（是否逐 token、行为细节因模型与实现而异）
- **批量**：`batch`
- **管道组合**：`a | b | c`

---

## 3. 标准方法（日常最常用）

Runnable 在接口层面**统一暴露**这些方法（具体行为由各类组件实现或委托框架完成）：

| 方法 | 作用 |
| :--- | :--- |
| **`.invoke(input)`** | 同步：**一个输入 → 一个输出**（最常用） |
| **`.stream(input)`** | 流式：按块产出，适合长文本、对话感 |
| **`.batch(inputs)`** | 批量：多份输入在同一条链上跑 |

异步对照（工程里写高并发时常用）：

| 方法 | 作用 |
| :--- | :--- |
| **`.ainvoke`** / **`.astream`** / **`.abatch`** | 与上表对应，异步版本 |

---

## 4. 常见哪些是 Runnable？

在 LangChain 日常开发里，**绝大部分你用来拼链的东西都是 Runnable**，例如：

- `PromptTemplate`、`ChatPromptTemplate`
- `LLM`、`ChatModel`
- `OutputParser`（如 `BaseOutputParser` 子类）
- **`prompt | model | parser` 整条链**（组合后仍是 Runnable）

**所以它们才能用 `|` 连在一起**：前一节的输出类型与后一节的输入类型要匹配（见 [05_prompt_template.md](./05_prompt_template.md) 里的类型对齐说明）。

---

## 5. 为什么要设计 Runnable？

LangChain 希望：**用法统一、心智模型统一。**

你不用先背「模板怎么调、模型怎么调、解析器怎么调」三套完全不同的 API——  
先认 **`Runnable`**：**会 `invoke`、可按需 `stream` / `batch`，能进管道**，再去看各组件的输入输出类型即可。

---

## 6. 极简总结（可复制到卡片）

### Runnable 是什么？

**LangChain 中可执行组件的统一接口标准**（在 `langchain_core` 的 Runnable 体系里落地）。

### 核心作用

- 提示词、模型、解析器、链：**同一套调用方式**
- 支持 **`.invoke()`**，以及 **`.stream()`**、**`.batch()`**（及 **`.ainvoke()`** 等异步）
- 支持用 **`|`** 拼成 **LCEL** 链

### 哪些是 Runnable？

`PromptTemplate`、`ChatModel`、`OutputParser`、整条 **`Chain`** 等，通常都是。

### 一句话终极版

**Runnable = 能按统一方式调用、能流式/批量、能进 `|` 管道的 LangChain 标准组件。**

---

## 7. 超短必背版（考试/面试一句）

**Runnable：LangChain 里可执行单元的统一接口；有 `invoke`（及 `stream`/`batch` 等），所以能用 `|` 串成链。**

---

## 延伸阅读

- [LCEL 组件组合](./07_lcel.md)  
- [环境搭建 & 核心概念](./01_env_and_core_concepts.md)
