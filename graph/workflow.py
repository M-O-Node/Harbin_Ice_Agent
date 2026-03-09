from langgraph.graph import StateGraph, END
from graph.state import AgentState
from agent.researcher import call_model, tool_executor

# 1. 初始化状态图
# 告诉 LangGraph 要用 AgentState 作为在各个节点间传递的数据结构
workflow = StateGraph(AgentState)

# 2. 添加节点 (Nodes)
# 节点就是我们要执行的动作. 咱们有两个动作: 大模型思考, 或者执行工具.
workflow.add_node('agent', call_model)  # 大脑节点
workflow.add_node('tools', tool_executor)  # 手脚节点

# 3. 定义起始点
# 流程一开始, 先把用户的消息扔给大脑 (agent 节点)
workflow.set_entry_point('agent')


### 条件路由 (Conditional Edge)
### Agent 最牛的地方: 会根据大脑的思考结果决定下一步, 而不是死板的往下走
def should_continue(state: AgentState) -> str:
    """
    判断逻辑:
    看大脑 (Agent) 最后给出的那条消息.
    如果消息里包括了 tool_calls (说明它想用工具), 就把流程导向 'tools' 节点.
    如果没有, 说明它已经得出结论了, 流程结束 ('END').
    :param state:
    :return:
    """
    last_message = state['messages'][-1]

    # 如果模型决定调用工具
    if last_message.tool_calls:
        return 'tools'

    # 否则, 结束
    return 'END'


# 4. 添加边 (Edge)
# 添加条件边: 大脑思考完之后, 走那条路?
workflow.add_conditional_edges(
    'agent',  # 从大脑节点出来
    should_continue,  # 经过判断函数
    {
        'tools': 'tools',  # 如果函数返回 'tools', 就走到 tools 节点
        'END': END,  # 如果返回 'END', 就结束流程
    },
)

# 添加普通边: 工具执行完之后, 去哪里?
# 工具执行完, 必须把结果拿回去给大脑再看一眼, 所以强制流回到 'agent' 节点
# 这就形成了一个 [思考-行动-观察] 的循环 (ReAct 机制)
workflow.add_edge('tools', 'agent')

# 5. 编译成可执行的程序
# 就像 Java 里的 build()
app = workflow.compile()

### 针对本文件的单元测试 Unit Test
if __name__ == '__main__':
    print('=== 开启哈尔滨冰雪智能体===')

    # 模拟用户提问
    # 故意问一个极其刁钻的, 必须结合私有知识和实时网络的问题
    test_query = '我是个南方小土豆，哈尔滨吃锅包肉去哪？另外帮我查一下冰雪大世界今天开门了吗？门票多少钱？'
    print(f'\n游客提问: {test_query}\n')

    # 初始化状态
    initial_state = {'messages': [('user', test_query)]}

    # stream() 会把图在运转时的每一步状态都打印出来
    # 可以清晰地看到它是怎么思考, 怎么调用工具的
    for output in app.stream(initial_state):
        # 打印当前走到哪个节点了
        for key, value in output.items():
            print(f'[{key} 节点执行完毕]')

            # 打印节点产生的最后一条消息
            last_msg = value['messages'][-1]

            # 如果是工具调用的消息, 打印出来
            if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                print(f'-> 大模型决定调用工具: {[t["name"] for t in last_msg.tool_calls]}')

            # 如果是工具执行完毕返回的结果
            elif last_msg.type == 'tool':
                print(f'<- 工具执行完毕, 返回结果: {last_msg.content[:100]}...')

            # 如果是大模型最终的回答
            elif last_msg.type == 'ai':
                print(f'ai 最终回答: {last_msg.content}')

    print('\n=== 流程结束 ===')
