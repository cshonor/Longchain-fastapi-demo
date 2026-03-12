import os
from pathlib import Path  # 处理文件路径，跨系统（Windows/Mac/Linux）兼容
from dotenv import load_dotenv  # 加载.env文件的核心库

# 从 longchain 目录加载 .env
# __file__ 指当前这个py文件的路径，parent是上级目录，最终找到同级的.env文件
_env_path = Path(__file__).parent / ".env"
# 加载.env文件，override=True表示如果系统环境变量有同名值，优先用.env里的
load_dotenv(_env_path, override=True)

# Deepseek 模型配置：从.env中读取密钥，没读到则为None
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# 读取接口地址，没读到则用默认值"https://api.deepseek.com"
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# 以下都是同理：为OpenAI/Anthropic/混元/通义千问/智谱AI加载密钥和接口地址
# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")

# 腾讯混元
HUNYUAN_APP_ID = os.getenv("HUNYUAN_APP_ID")
HUNYUAN_SECRET_ID = os.getenv("HUNYUAN_SECRET_ID")
HUNYUAN_SECRET_KEY = os.getenv("HUNYUAN_SECRET_KEY")

# 阿里通义千问（Dashscope）
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
DASHSCOPE_BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mod/v1")

# 智谱AI
ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")
ZHIPUAI_BASE_URL = os.getenv("ZHIPUAI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")