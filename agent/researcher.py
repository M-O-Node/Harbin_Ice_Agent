import os
from dotenv import load_dotenv

# 加载配置
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
# 引入 LangGraph 预置的 ToolNod, 它能自动把我们的函数包装成可执行的图节点
from langgraph.prebuilt import ToolNode

# 引入我们刚才构建的两只手
from tools.tavily_search import tavily_tool
from tools.milvus_rag import search_local_knowledge

# 1. 组装工具箱 (List of Tools)
tools = [tavily_tool, search_local_knowledge]

# 2. 实例化大脑 (依然使用 1.0 使用的 72B)
SILICON_KEY = os.getenv('OPENAI_API_KEY')
SILICON_BASE_URL = os.getenv('OPENAI_API_BASE_URL')

llm = ChatOpenAI(
    api_key=SILICON_KEY,
    base_url=SILICON_BASE_URL,
    model='Qwen/Qwen2.5-72B-Instruct',
    temperature=0.7,
)

# 3. 给大脑绑定工具 (Bind Tools)
llm_with_tools = llm.bind_tools(tools)

# 4. 定义 Agent 的处理节点 (核心逻辑)
from graph.state import AgentState


def call_model(state: AgentState):
    """
    这是大脑的运转逻辑: 读取历史消息 -> 决定是回答还是调用工具 -> 生成新消息
    :param state:
    :return:
    """
    print('\n[大脑运转中] 正在思考如何回复或是否需要使用工具...')

    message = state['messages']

    # 给 Agent 加上人设和系统提示词 (Persona) 角色
    sys_msg = SystemMessage(content="""
    你是哈尔滨最懂行的金牌旅游向导 "冰城老铁". 你热情, 幽默, 偶尔带点东北口音. 
    你有两个得力助手 (工具):
    1. search_local_knowledge: 专门查历史攻略, 避坑指南, 美食推荐 (本地库). 
    2. tavily_search_result_json: 专门查今天的天气, 最新的票价, 门票是否开售等 (实时网).
    
    面对南方小土豆的复杂问题, 如果本地库没有, 一定要善用实时搜索. 
    最终的回答必须条理清晰
    """)

    # 将系统提示词放在最前面, 加上之前的对话历史
    response = llm_with_tools.invoke([sys_msg] + message)

    # 返回新的状态 (追加消息)
    return {'messages': [response]}


# 5. 实例化工具执行节点
# 刚才大模型只负责 "发出调用指令", 而这个 ToolNode 负责真正 "执行代码"
tool_executor = ToolNode(tools)
