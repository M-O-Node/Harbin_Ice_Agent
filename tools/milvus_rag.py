import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)

import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.vectorstores import Milvus
from langchain_huggingface import HuggingFaceEmbeddings

# 加载 .env 文件中的配置
load_dotenv()

# 读取 Milvus 配置
ALIYUN_IP = os.getenv('MILVUS_HOST', '127.0.0.1')
MILVUS_PORT = os.getenv('MILVUS_PORT', '19530')

# 1. 初始化 Embedding 模型 (那个 1.0 中用过的模型)
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# 2. 连接 Milvus
vector_db = Milvus(
    embeddings,
    connection_args={'host': ALIYUN_IP, 'port': MILVUS_PORT},
    collection_name='harbin_agent_kb',  # 1.0 用过的
)


### @tool 装饰器 核心魔法
### 加上这个装饰器, 它就从一个普通的 method 变成一个暴露给 LLM 的 API 接口
@tool
def search_local_knowledge(query: str) -> str:
    """
    当询问关于哈尔滨旅游的 [历史经验], [避坑指南], [穿搭建议], [美食推荐]时调用该方法
    去本地私有知识库中搜索最正宗的攻略
    :param query:
    :return:
    """
    print(f'\n[Milvus Tool 执行中] 正在去私有知识库检索: {query}')

    # 搜索 3 条经验
    docs = vector_db.similarity_search(query, k=3)

    if not docs:
        return '私有知识库中没有找到相关信息. '

    # 将找到的结果拼接成字符串返回给 Agent
    result = '\n'.join([f'- {doc.page_content}' for doc in docs])

    return result


# 仅用于本文件单独测试 Unit Test
if __name__ == '__main__':
    print('正在测试 Milvus 工具')
    # 这里我们直接 invoke, 模拟大模型调用这个工具
    test_result = search_local_knowledge.invoke({'query': '哈尔滨吃锅包肉去哪?'})

    print('\n=== 从 Milvus 捞回来的结果 ===')
    print(test_result)
