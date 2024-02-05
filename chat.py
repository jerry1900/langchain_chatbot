import streamlit as st

from chain import generate_response

# with st.chat_message('user',avatar='🤖'):
#     st.write('hello there')
#
# prompt = st.chat_input('聊天什么吧')
# if prompt:
#     st.write(f"用户说：{prompt}")

st.title('🤖AI小万的旅游聊天机器人😜')

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 展示聊天记录
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"], avatar='☺️'):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"], avatar='🤖'):
            st.markdown(message["content"])

# 用于用户输入
if prompt := st.chat_input('What is up'):
    with st.chat_message('user', avatar='☺️'):
        st.markdown(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    answer = generate_response(prompt)

    response = answer['text']

    with st.chat_message('assistant', avatar='🤖'):
        st.markdown(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
