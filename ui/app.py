import streamlit as st
import sys
import os

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
    st.session_state.agent_messages.append(('user', user_input))

    # 2. 调用 Agent 大脑
    with st.chat_message('assistant'):
        # 用一个旋转的菊花表示正在思考
        with st.spinner('老铁正在疯狂搜集情报, 稍等...'):
            # 构建初始状态传给图
            initial_state = {'messages': st.session_state.agent_messages}

            # 运行工作流, 拿到最终状态
            # 这里我们不用 stream, 直接用 invoke 拿到最后的结果
            final_state = agent_app.invoke(initial_state)

            # 提取最后一条 AI 说的话
            final_response = final_state['messages'][-1].content

            # 把新的消息更新到记忆里, 为了下一轮对话
            st.session_state.agent_messages = final_state['messages']

        # 在界面上打印结果
        st.markdown(final_response)
        st.session_state.messages.append({'role': 'assistant', 'content': final_response})
