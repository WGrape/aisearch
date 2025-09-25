"""
@File: aisearch_by_langchain_agent.py
@Date: 2024/12/10 10:00
@Desc: 基于Langchain的Agent实现AI搜索
"""
import os
import sys
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_core.prompts.chat import ChatPromptTemplate
from web_search import SearchWebTool, OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
from langchain.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 创建model模型
model = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0.5,
    timeout=None,
    max_retries=3,
    api_key=OPENAI_API_KEY,  # 配置你的api_key
    base_url=OPENAI_BASE_URL,
    streaming=False,
)

system_message_prompt = SystemMessagePromptTemplate.from_template(template="# 角色\n你是一个智能助手")
human_message_prompt = HumanMessagePromptTemplate.from_template(template="# 用户问题\n{input}\n{agent_scratchpad}")  # 必须使用agent_scratchpad这个变量
chat_prompt_template = ChatPromptTemplate.from_messages(messages=[
    system_message_prompt, human_message_prompt,
])

# 创建工具
tools = [
    SearchWebTool()
]

# 第一种使用方法[可以使用]
# agent = create_openai_tools_agent(llm=model, tools=tools, prompt=chat_prompt_template)
# executor = AgentExecutor(agent=agent, tools=tools)

# 第二种使用方法[可以使用]
agent = create_tool_calling_agent(llm=model, tools=tools, prompt=chat_prompt_template)
executor = AgentExecutor(agent=agent, tools=tools)

# 调用链
print("1: ", executor.invoke({"input": "搜索北京今天的天气"}))
