import os
from dotenv import load_dotenv

# # 针对魔法访问
# PROXY_URL = 'http://127.0.0.1:3066'
#
# os.environ['http_proxy'] = PROXY_URL
# os.environ['https_proxy'] = PROXY_URL
# os.environ['HTTP_PROXY'] = PROXY_URL
# os.environ['HTTPS_PROXY'] = PROXY_URL

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

"""
Calling Tavily Agent messages !!!
关键词搜索: 今天哈尔滨冰雪大世界开门了吗? 门票多少钱?
Return Intelligence...
{'query': '今天哈尔滨冰雪大世界开门了吗? 门票多少钱?', 'follow_up_questions': None, 'answer': '哈尔滨冰雪大世界将于2025年12月17日开园，12月17日-23日票价298元，12月24日起票价恢复328元。', 'images': [], 'results': [{'url': 'https://m.gmw.cn/2023-12/02/content_1303588437.htm', 'title': '官宣！哈尔滨冰雪大世界票价出炉！咋去最划算？看这里→', 'content': '据介绍，哈尔滨冰雪大世界正式营业以后，标准成人门票价格为328元/人，可以提前预约游玩超级大滑梯、雪花摩天轮、滑雪体验区域等项目，可以预约观看哈冰秀、', 'score': 0.85097736, 'raw_content': None}, {'url': 'https://beer.hrbicesnow.com/m/yunying', 'title': '营业时间每日11:00开园，22:00闭园。 - 哈尔滨冰雪大世界', 'content': '营业时间每日11:00开园，22:00闭园。 ; 标准成人门票：328元/人 ; 优惠票：240元/人 ; 畅享票畅享票：800元/张.', 'score': 0.81630427, 'raw_content': None}, {'url': 'https://news.qq.com/rain/a/20260219A063G700', 'title': '哈尔滨冰雪大世界门票价格调整！-腾讯新闻', 'content': '2026年2月20日（正月初四）、2月21日（正月初五）临时闭园；2月22日（正月初六）17时拟恢复运营，营业时间将延时至当日24时。重新开园后标准成人票调整为228元/张，', 'score': 0.7031221, 'raw_content': None}], 'response_time': 1.29, 'request_id': '78a9e10d-259c-47af-abee-d4ea05185538'}
"""