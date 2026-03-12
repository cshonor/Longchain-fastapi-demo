from langchain.chat_models import init_chat_model
from langchain_deepseek import ChatDeepSeek

from longchain.env_utils import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# 两种方式创建大模型对象
# 1. 直接使用模型类
deepseek_llm = ChatDeepSeek(
    api_key=DEEPSEEK_API_KEY,      # API 密钥，用于身份认证
    base_url=DEEPSEEK_BASE_URL,    # API 请求地址，代理/中转时需修改
    model="deepseek-chat",         # 模型名：deepseek-chat 对话模型，deepseek-reasoner 推理模型
)

# 2. 通过 LangChain 统一通用方式 init_chat_model
# llm_unified = init_chat_model(
#     model="deepseek-chat",
#     model_provider="deepseek",
#     api_key=DEEPSEEK_API_KEY,
#     base_url=DEEPSEEK_BASE_URL,
# )

if __name__ == "__main__":
    resp = deepseek_llm.invoke("你好")
    print(type(resp))
    print(resp.content)
