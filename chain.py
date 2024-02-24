from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from template import STAGE_ANALYZER_INCEPTION_PROMPT,BASIC_TEMPLATE,RECOMMEND_TEMPLATE

class StageAnalyzerChain(LLMChain):
    """通过查看聊天记录判断是否要转向推荐和销售阶段."""

    @classmethod
    def from_llm(cls, llm, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        stage_analyzer_inception_prompt_template = STAGE_ANALYZER_INCEPTION_PROMPT
        prompt = PromptTemplate(
            template=stage_analyzer_inception_prompt_template,
            input_variables=[
                "conversation_history",
                "question"
            ],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)

class ConversationChain_Without_Tool(LLMChain):
    #当用户没有明确的感兴趣话题时，用这个chain和用户闲聊
    @classmethod
    def from_llm(cls, llm, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        conversation_without_tools_template = BASIC_TEMPLATE
        prompt = PromptTemplate(
            template=conversation_without_tools_template,
            input_variables=[
                "conversation_history",
            ],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)

class Recommend_Product(LLMChain):
    #当用户有明确的感兴趣话题时，用这个chain查询产品库，看是否命中，如果命中则生成一个产品推荐信息

    @classmethod
    def from_llm(cls, llm, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        conversation_without_tools_template = RECOMMEND_TEMPLATE
        prompt = PromptTemplate(
            template=conversation_without_tools_template,
            input_variables=[
                "conversation_history",
            ],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)

