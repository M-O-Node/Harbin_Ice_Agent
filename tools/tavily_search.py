import os
from dotenv import load_dotenv

# 1. 加载 .env 里面的环境变量 (拿到 Tavily Key)
load_dotenv()

# 2. 引入官方最新的 Tavily 工具
from langchain_tavily import TavilySearch

# 3. 实例化工具
# max_result=3: 每次搜索只取最相关的 3 条结果
# include_answer=True: 让 Tavily 不仅给链接, 还给个总结
tavily_tool = TavilySearch(max_results=3, include_answer=True)

# 仅用于本文件单独测试 (Unit Test)
if __name__ == '__main__':
    print('Calling Tavily Agent messages !!!')

    # 模拟 Agent 要搜的问题
    # 注意: Tavily 的能力在于查 "实时数据", 而不是死攻略
    query = '今天哈尔滨冰雪大世界开门了吗? 门票多少钱?'
    print(f'关键词搜索: {query}')

    # invoke 就是执行工具
    result = tavily_tool.invoke({'query': query})

    print('Return Intelligence...')
    print(result)

