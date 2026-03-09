import streamlit as st
import sys
import os
from langchain_core.messages import HumanMessage, AIMessage

# 确保能导入外层目录的模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入咱们刚才写好的工作流
from graph.workflow import app as agent_app

# --- 页面配置 ---
st.set_page_config(page_title='哈尔滨冬季智能导游', page_icon='❄', layout='centered')
st.title('❄ 哈尔滨冬季智能导游 (Agent 2.0)')
st.caption('我是你的东北老铁，本地攻略、实时票价、天气，问我就对啦！')

# --- 初始化 Session 记忆 ---
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # 给 Agent 注入一条初始的系统设定, 让它保持人设
    st.session_state.agent_messages = []

# --- 渲染历史聊天记录 ---
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# --- 接受用户输入 ---
if user_input := st.chat_input('问点啥？比如：哈尔滨今天冷吗？哪的锅包肉好吃？'):
    # 1. 把用户的话显示在界面上
    with st.chat_message('user'):
        st.markdown(user_input)
    st.session_state.messages.append({'role': 'user', 'content': user_input})

    # 把用户的话加到 Agent 的记忆里
    st.session_state.agent_messages.append(HumanMessage(content=user_input))

    # 2. 调用 Agent 大脑
    with st.chat_message('assistant'):
        status_placeholder = st.empty()
        status_placeholder.info('❄ 冰城老铁正在疯狂搜集情报, 稍等...')

        response_placeholder = st.empty()
        full_response = ''

        # 4. 执行 Agent 流程
        for event in agent_app.stream({'messages': st.session_state.agent_messages}):
            for key, value in event.items():
                if key == 'agent':
                    # 记录大脑的思考
                    last_msg = value['messages'][-1]
                    if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                        tool_names = [t['name'] for t in last_msg.tool_calls]
                        status_placeholder.warning(f'🔧 老铁决定使用工具: {tool_names}')

                    elif hasattr(last_msg, 'content') and last_msg.content:
                        full_response += last_msg.content
                        response_placeholder.markdown(full_response + '| ')

                elif key == 'tools':
                    # 记录日志, 执行结果
                    tool_output = value['messages'][-1].content
                    status_placeholder.success('√ 工具执行完毕, 情报已整合!!!')

        # 完成后清理
        status_placeholder.empty()
        st.session_state.messages.append({'role': 'assistant', 'content': full_response})
        st.session_state.agent_messages.append(AIMessage(content=full_response))
