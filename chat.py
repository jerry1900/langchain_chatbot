import io
import streamlit as st
from PIL import Image

from agent import ConversationAgent, welcome_agent,fake_system

st.title('🤖AI小万的旅游聊天机器人😜')

with st.sidebar:
    # 设置一个可点击打开的展开区域
    with st.expander("🤓国内可访问的openai账号"):
        st.write("""
            1. 如果使用默认地址，可以使用openai官网账号（需科学上网🥵）.
            2. 如果你没有openai官网账号，可以联系博主免费试用国内openai节点账号🥳.
        """)

        # 本地图片无法直接加载，需先将图片读取加载为bytes流，然后才能正常在streamlit中显示
        image_path = r"C:\Users\Administrator\langchain_chatbot\wechat.jpg"
        image = Image.open(image_path)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        st.image(image_bytes, caption='AI小万老师的微信', use_column_width=True)

    st.markdown('1. 每次加载有不同的欢迎词')
    st.markdown('2. 当你连续询问关于北京、上海和美国的信息后，会给你推荐旅游产品')


# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

if "welcome_word" not in st.session_state:
    st.session_state.welcome_word = welcome_agent()
    st.session_state.messages.append({'role': 'assistant', 'content': st.session_state.welcome_word['text']})
    st.session_state.agent = ConversationAgent()
    st.session_state.agent.seed_agent()
    st.session_state.agent.generate_stage_analyzer(verbose=True)

# 展示聊天记录
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"], avatar='☺️'):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"], avatar='🤖'):
            st.markdown(message["content"])

# 用于用户输入
if prompt := st.chat_input('我们来聊一点旅游相关的事儿吧'):

    with st.chat_message('user', avatar='☺️'):
        st.markdown(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    st.session_state.agent.determine_conversation_stage(prompt)
    st.session_state.agent.human_step(prompt)
    response = st.session_state.agent.step()

    with st.chat_message('assistant', avatar='🤖'):
        st.markdown(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
