from typing import Any, Callable, Dict, List, Union
import streamlit as st

from pydantic import Field
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import LLMSingleActionAgent,AgentExecutor

from chain import StageAnalyzerChain,ConversationChain_Without_Tool
from stages import CONVERSATION_STAGES
from my_tools import *
from template import *


def welcome_agent():
    llm = OpenAI(
        temperature=0.6,
        # openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_key=st.secrets['api']['key'],
        # base_url=os.getenv("OPENAI_BASE_URL")
        base_url=st.secrets['api']['base_url']
    )

    prompt = PromptTemplate.from_template(WELCOME_TEMPLATE)

    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,

    )

    response = chain.invoke("简短的欢迎词")

    return response


def fake_system():
    fake_message = {'text':'模拟输出'}
    return fake_message

class ConversationAgent():
    stage_analyzer_chain: StageAnalyzerChain = Field(...)
    conversation_agent_without_tool = Field()
    conversation_agent_with_tool = Field()

    conversation_history = []
    conversation_stage_id: str = "1"
    current_conversation_stage: str = CONVERSATION_STAGES.get("1")

    llm = OpenAI(
            temperature=0,
            openai_api_key=st.secrets['api']['key'],
            base_url=st.secrets['api']['base_url']
         )

    def seed_agent(self):
        self.conversation_history.clear()
        print("——Seed Successful——")

    def show_chat_history(self):
        return self.conversation_history

    def retrieve_conversation_stage(self, key):
        return CONVERSATION_STAGES.get(key)

    def fake_step(self):
        input_text = self.conversation_history[-1]
        ai_message = self._respond_with_tools(str(input_text), verbose=True)
        print(ai_message,type(ai_message['output']))

    def step(self):
        input_text = self.conversation_history[-1]
        print(str(input_text)+'input_text****')

        if int(self.conversation_stage_id) == 1:
            ai_message = self._respond_without_tools(str(input_text),verbose=True)
        else:
            chat_message = self._respond_without_tools(str(input_text), verbose=True)
            recommend_message = self.recommend_product()
            print(recommend_message,len(recommend_message))
            if len(recommend_message)<=5:
                ai_message = chat_message
            else:
                ai_message = chat_message + '\n\n' + recommend_message
            # output_dic = self._respond_with_tools(str(input_text),verbose=True)
            # ai_message = str(output_dic['output'])

        print(ai_message,type(ai_message))

        ai_message = "AI:"+str(ai_message)
        self.conversation_history.append(ai_message)
        # print(f"——系统返回消息'{ai_message}'，并添加到history里——")
        return ai_message.lstrip('AI:')

    def human_step(self,input_text):
        human_message = input_text
        human_message = "用户: " + human_message
        self.conversation_history.append(human_message)
        # print(f"——用户输入消息'{human_message}'，并添加到history里——")
        return human_message

    def generate_stage_analyzer(self,verbose: bool = False):
        self.stage_analyzer_chain = StageAnalyzerChain.from_llm(
            llm=self.llm,
            verbose=verbose
        )

        print("成功构造一个StageAnalyzerChain")


    def determine_conversation_stage(self,question):
        self.question = question
        print('-----进入阶段判断方法-----')
        self.conversation_stage_id = self.stage_analyzer_chain.run(
            conversation_history=self.conversation_history,
            question=self.question
        )

        print(f"Conversation Stage ID: {self.conversation_stage_id}")
        print(type(self.conversation_stage_id))
        self.current_conversation_stage = self.retrieve_conversation_stage(
            self.conversation_stage_id
        )
        print(f"Conversation Stage: {self.current_conversation_stage}")

    def _respond_without_tools(self,input_text,verbose: bool = False):
        self.conversation_agent_without_tool = ConversationChain_Without_Tool.from_llm(
            llm=self.llm,
            verbose=verbose
        )

        response = self.conversation_agent_without_tool.run(
            question = input_text,
            conversation_history=self.conversation_history,
        )

        return response
    def get_tools(self):
        file_path = r'C:\Users\Administrator\langchain_chatbot\product.txt'
        knowledge_base = build_knowledge_base(file_path)
        tools = get_tools(knowledge_base)
        return tools


    def recommend_product(self,verbose =True):

        tools = self.get_tools()

        prompt = CustomPromptTemplateForTools(
            template=RECOMMEND_TEMPLATE,
            tools_getter=lambda x: tools,
            # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
            # This includes the `intermediate_steps` variable because that is needed
            input_variables=[
                "intermediate_steps",  # 这是在调用tools时，会产生的中间变量，是一个list里面的一个tuple，一个是action，一个是observation
                "conversation_history",
            ],
        )

        llm_chain = LLMChain(llm=self.llm, prompt=prompt, verbose=verbose)

        tool_names = [tool.name for tool in tools]

        # WARNING: this output parser is NOT reliable yet
        ## It makes assumptions about output from LLM which can break and throw an error
        output_parser = SalesConvoOutputParser()

        recommend_agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names,

        )

        sales_agent_executor = AgentExecutor.from_agent_and_tools(
            agent=recommend_agent, tools=tools, verbose=verbose, max_iterations=5
        )

        inputs = {
            "conversation_history": "\n".join(self.conversation_history),
        }

        response = sales_agent_executor.invoke(inputs)

        return str(response['output'])









