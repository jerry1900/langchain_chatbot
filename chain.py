import os

import streamlit as st

from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

from template import BASIC_TEMPLATE

def build_chain(memory):
    llm = OpenAI(
        temperature=0,
        # openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_key=st.secrets['api']['key'],
        # base_url=os.getenv("OPENAI_BASE_URL")
        base_url=st.secrets['api']['base_url']
    )

    prompt = PromptTemplate.from_template(BASIC_TEMPLATE)


    conversation = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=memory,

    )

    return conversation

def generate_response(chain,input_text):

    response = chain.invoke(input_text)
    return  response