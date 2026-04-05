"""
Output Parser（含 prompt | llm | parser）— 对应 06_output_parser.md

在仓库根目录执行:
  python langchain-learning-notes/02_langchain_first_experience/demo_output_parser.py

无需 Key: 自定义解析器 + 内置解析器对模拟字符串的 parse。
需 DASHSCOPE_API_KEY: PromptTemplate | Tongyi | CommaSeparatedListOutputParser
"""

from __future__ import annotations

import os
from pathlib import Path

from langchain_core.output_parsers import BaseOutputParser

_ROOT = Path(__file__).resolve().parents[2]
try:
    from dotenv import load_dotenv

    load_dotenv(_ROOT / ".env")
except ImportError:
    pass


class CustomCommaListParser(BaseOutputParser[list[str]]):
    """教学用：继承 BaseOutputParser，与 06_output_parser.md 示例一致。"""

    def parse(self, text: str) -> list[str]:
        return [item.strip() for item in text.strip().split(",") if item.strip()]


def demo_parse_offline() -> None:
    from langchain_core.output_parsers import CommaSeparatedListOutputParser

    raw = "杯语, 暖杯坊, 水韵"
    custom = CustomCommaListParser()
    builtin_parser = CommaSeparatedListOutputParser()
    print("[1] 离线 parse（自定义 BaseOutputParser vs 内置 CommaSeparatedListOutputParser）")
    print("  原始:", raw)
    print("  自定义 parse: ", custom.parse(raw))
    print("  内置 parser:  ", builtin_parser.parse(raw))
    print("  format_instructions 示例:", builtin_parser.get_format_instructions()[:80] + "...")
    print()


def demo_chain() -> None:
    key = os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        print("[2] LCEL chain — 跳过：未设置 DASHSCOPE_API_KEY\n")
        return

    try:
        from langchain_community.llms.tongyi import Tongyi
    except ImportError:
        print("[2] LCEL chain — 跳过：未安装 langchain-community\n")
        return

    from langchain_core.output_parsers import CommaSeparatedListOutputParser
    from langchain_core.prompts import PromptTemplate

    parser = CommaSeparatedListOutputParser()
    prompt = PromptTemplate.from_template(
        "{format_instructions}\n\n产品：{product}。"
        "请只输出 3 个简短的中文公司名，英文逗号分隔，不要编号、不要解释。"
    )
    llm = Tongyi(api_key=key)
    chain = prompt | llm | parser

    names = chain.invoke(
        {
            "format_instructions": parser.get_format_instructions(),
            "product": "保温杯",
        }
    )
    print("[2] prompt | Tongyi | CommaSeparatedListOutputParser")
    print("  结果类型:", type(names).__name__)
    print("  结果:", names)
    print()


def main() -> None:
    os.chdir(_ROOT)
    print("工作目录:", _ROOT)
    print("对应笔记: langchain-learning-notes/02_langchain_first_experience/06_output_parser.md")
    print("-" * 60)
    demo_parse_offline()
    demo_chain()


if __name__ == "__main__":
    main()
