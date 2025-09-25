"""
@File: aisearch_by_manual_workflow.py
@Date: 2024/12/10 10:00
@Desc: 基于手动Workflow的AI搜索实现
"""
import os
import sys
from wpylib.util.x.xjson import parse_raise
from wpylib.pkg.langchain.model import Model
from wpylib.pkg.langchain.chain import create_chain
from web_search import search_web_tool, MODEL_CONFIG
from wpylib.pkg.langchain.prompt import create_chat_prompt_by_messages
from langchain_core.prompts.chat import SystemMessage, HumanMessage, HumanMessagePromptTemplate

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

model = Model(
    model_type=MODEL_CONFIG["model_type"],
    model_config=MODEL_CONFIG,
)


def analyze_query(query: str) -> list[str]:
    """
    分析用户输入, 并返回分析后的Query列表
    :param query: 用户输入的问题
    :return: 返回分析处理后的query
    """
    # (1) 意图分析
    prompt = create_chat_prompt_by_messages(messages=[
        SystemMessage(content="""
    # 角色
    你是一个意图分析器。
    # 要求
    请分析用户的意图，属于以下类别之一：
    - method
    - write
    - summary
    - none
    # 返回格式
    请以以下JSON格式返回：
    {
        "intention": "<类别>"
    }
    """),
        HumanMessagePromptTemplate.from_template("{input}"),
    ])
    chain = create_chain(
        model=model.get_raw_model(),
        prompt=prompt,
    )
    llm_invoke = chain.invoke(input=query)
    llm_result = parse_raise(llm_invoke["text"].replace("\n", ""))
    intention = llm_result["intention"]
    # 可以基于不同的意图, 自定义扩展后续的回答逻辑

    # (2) Query改写
    prompt = create_chat_prompt_by_messages(messages=[
        SystemMessage(content="""
    # 角色
    你是一个查询改写器。
    # 要求
    请对此查询进行改写，包括但不限于错字更正、歧义消除等。
    # 返回格式
    请以以下JSON格式返回：
    {
        "rewritten_query": "<改写后的查询>"
    }
    """),
        HumanMessagePromptTemplate.from_template("{input}"),
    ])
    chain = create_chain(
        model=model.get_raw_model(),
        prompt=prompt,
    )
    llm_invoke = chain.invoke(input=query)
    llm_result = parse_raise(llm_invoke["text"].replace("\n", ""))
    rewritten_query = llm_result["rewritten_query"]

    # (3) Query扩写
    prompt = create_chat_prompt_by_messages(messages=[
        SystemMessage(content="""
    # 角色
    你是一个查询扩写器。
    # 要求
    请对此查询进行扩写，包括但不限于同义词扩写、相近概念扩写等。
    # 返回格式
    请以以下JSON格式返回：
    {
        "expanded_query": ["<扩写后的查询>"]
    }
    """),
        HumanMessagePromptTemplate.from_template("{input}"),
    ])
    chain = create_chain(
        model=model.get_raw_model(),
        prompt=prompt,
    )
    llm_invoke = chain.invoke(input=rewritten_query)
    llm_result = parse_raise(llm_invoke["text"].replace("\n", ""))
    query_list = llm_result["expanded_query"][:3]

    # 返回分析并处理后的Query列表
    return query_list


def search_query(query_list: list[str]) -> str:
    """
    执行搜索
    :param query_list: 处理后的Query列表
    :return: 返回搜索结果内容
    """
    search_context = ""
    for temp_query in query_list:
        search_context += search_web_tool(query=temp_query) + "\n"
    return search_context


def generate_answer(query: str, search_context: str) -> str:
    """
    生成回答
    :param query: 用户输入的问题
    :param search_context: 搜索结果内容
    :return: 返回模型回答内容
    """
    # 调用模型回答
    llm_text_generator = model.stream(
        langchain_input=[
            # System消息
            SystemMessage(
                content="# 角色\n你是一个智能助手 ## 要求\n请基于以下搜索结果，回答用户的问题。\n\n### 搜索结果\n" + search_context
            ),
            # 加入当前用户提问
            HumanMessage(query)
        ]
    )

    # 输出内容
    llm_text = ""
    for item in llm_text_generator:
        llm_text += item.content
        print(item.content, end="", flush=True)
    return llm_text


def aisearch_workflow(query: str) -> str:
    """
    开始执行AI搜索工作流
    :param query: 用户输入的问题
    """
    # [分析输入部分]分析用户输入
    query_list = analyze_query(query=query)

    # [执行动作部分]开始执行搜索
    search_context = search_query(query_list=query_list)

    # [生成答案部分]调用模型回答
    llm_text = generate_answer(query=query, search_context=search_context)
    return llm_text


user_ask = "搜索北京今天的天气"
answer = aisearch_workflow(query=user_ask)
print(f"\n\nAnswer: {answer}")
