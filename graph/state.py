import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage


# 定义整个 Agent 的全局状态 (记忆本)
# TypedDict 就像是 Java 里的 DTO
class AgentState(TypedDict):
    # messages: 存放用户和 Agent 所有的聊天记录
    # Annotated[Sequence[BaseMessage], operator.add]: 这是个神奇的语法, 意思是每当有新的消息进来, 追加到原来列表后面.
    # 这就是 Agent 拥有 "记忆" 的底层原理!
    messages: Annotated[Sequence[BaseMessage], operator.add]

    # 还可以存一些我们需要中间传递的变量, 例如用户的原始意图
    current_intent: str
