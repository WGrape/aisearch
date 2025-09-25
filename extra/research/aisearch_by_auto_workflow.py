"""
@File: aisearch_by_auto_workflow.py
@Date: 2024/12/10 10:00
@Desc: 基于自动Workflow的AI搜索实现
"""
import os
import sys
from typing import Any
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


class Plan:
    """
    规划实体类: 分析器生成的结果封装
    """
    _type: str
    _desc: str
    _query: str
    _part: str

    def __init__(self, type: str, desc: str, query: str, part: str):
        """
        初始化实体
        :param type: 动作类型
        :param desc: 动作的描述
        :param query: 查询词
        :param part: 每一部分的输出标题
        """
        self._type = type
        self._desc = desc
        self._query = query
        self._part = part

    def get_type(self) -> str:
        """
        返回_type属性
        :return:
        """
        return self._type

    def get_desc(self) -> str:
        """
        返回_desc属性
        :return:
        """
        return self._desc

    def get_query(self) -> str:
        """
        返回_query属性
        :return:
        """
        return self._query

    def get_part(self) -> str:
        """
        返回_part属性
        :return:
        """
        return self._part


class Analyzer:
    """
    分析器类: 对用户输入的分析
    """
    _model: Any

    def __init__(self):
        # 完成动作类的初始化
        self._model = model

    def analyze(self, query: str) -> list[Plan]:
        """
        开始分析
        :param query: 用户输入的查询词
        :return:
        """
        prompt = create_chat_prompt_by_messages(messages=[
            SystemMessage(content="""
# 角色
你是一个对用户提问做分析和深度意图挖掘，并动态给出规划的助手。
## 目标
对用户提问做分析和深度意图挖掘，并动态给出相应的规划。
## 可选择的意图
- method ：比如 ”如何零基础学习唱歌“，”如何学习大模型技术“，”如何自学高等数学“。
- write ：比如 ”帮我写个短篇小说“，”给我写篇关于大模型技术的博客“，”帮我写篇关于春天的自媒体文章“。
- summary ：比如 ”天空为什么是蓝色的“，”为什么大模型会出现幻觉“。
- none ：无任务意图，比如 ”你好啊“，”请问你是谁啊“。
## 可选择的动作
- 联网搜索并输出:  {{"type": "search_web_and_output", "keyword": "the search keyword", "part": "which part does the output belong to"}}
- 仅输出:  {{"type": "output", "part": "which part does the output belong to"}}
- 结束:  {{"type": "end"}}
## 示例
### 教我零基础学习Python语言
```json
{
    "thought": "嗯，你向我询问学习Python编程语言。考虑到你零基础，可能从事非计算机领域。所以，我在回答前，我会先帮你联网搜索并解释编程语言和计算机领域的关系，接着我会联网搜索编程语言的作用。然后我开始正式回答你的问题，开始联网搜索并告诉你Python语言的基础知识和学习方法，再帮你联网搜索和推荐一些相关的学习课程，最后我自己给你一些Python语言的编程案例供你学习使用。",
    "plan": [
        {"type": "search_web_and_output", "keyword": "编程语言和计算机领域的关系", "part": "编程语言的背景"},
        {"type": "search_web_and_output", "keyword": "编程语言的作用", "part": "编程语言的作用"},
        {"type": "search_web_and_output", "keyword": "Python语言的基础知识", "part": "基础知识"},
        {"type": "search_web_and_output", "keyword": "Python语言的学习方法", "part": "学习方法"},
        {"type": "search_web_and_output", "keyword": "Python语学习课程推荐", "part": "课程推荐"},
        {"type": "search_web_and_output", "keyword": "Python编程案例", "part": "编程案例"},
        {"type": "output", "part": "总结"},
        {"type": "end"}
    ],
    "intention": "method"
}
```
## 要求
1. 如果提问意图为”method“，必须按照有顺序、有逻辑条理的方式来解答。
2. 如果提问意图为”summary“，则必须在正面回答问题的前提下，自行规划。
        """),
            HumanMessagePromptTemplate.from_template("{input}"),
        ])
        chain = create_chain(
            model=self._model.get_raw_model(),
            prompt=prompt,
        )
        llm_invoke = chain.invoke(input=query)
        llm_result = parse_raise(llm_invoke["text"].replace("\n", ""))
        print(llm_result)

        # 返回结果
        plan_list: list[Plan] = []
        for item in llm_result["plan"]:
            plan_list.append(Plan(
                type=item["type"], desc=item.get("desc", ""), query=item.get("keyword", ""), part=item.get("part", "")
            ))
        return plan_list


class OutputAction:
    """
    动作类: 仅输出动作的实现
    """
    _model: Any

    def __init__(self):
        # 完成动作类的初始化
        self._model = model

    def output(self, plan: Plan, search_context: str) -> str:
        """
        开始输出
        :param plan: 规划实体
        :param search_context: 联网搜索结果
        :return:
        """
        llm_text_generator = self._model.stream(
            langchain_input=[
                # System消息
                SystemMessage(
                    content="# 角色\n你是一个智能助手 ## 要求\n请基于以下搜索结果，回答用户的问题。\n\n### 搜索结果\n" + search_context
                ),
                # 加入当前用户提问
                HumanMessage(plan.get_query())
            ]
        )

        # 获取标题部分并打印
        header = f"## {plan.get_part()}\n"
        print(header, end="", flush=True)

        # 拼接内容并打印
        llm_text = header
        for item in llm_text_generator:
            content = item.content
            print(content, end="", flush=True)
            llm_text += content

        # 打印换行符并添加到最终文本
        footer = "\n"
        print(footer)
        llm_text += footer
        return llm_text


class SearchWebAndOutputAction:
    """
    动作类: 联网搜索且输出动作的实现
    """
    _output_action: OutputAction

    def __init__(self):
        self._output_action = OutputAction()

    def search_web_and_output(self, plan: Plan, count: int = 5) -> (str, str):
        """
        开始搜索
        :param plan: 规划实体
        :param count: 联网检索的数量
        :return:
        """
        search_context = search_web_tool(query=plan.get_query(), count=count)
        output = self._output_action.output(plan=plan, search_context=search_context)
        return search_context, output


class WorkFlow:
    """
    工作流类: 执行分析器生成的规划
    """
    _output_action: OutputAction
    _search_web_and_output_action: SearchWebAndOutputAction

    def __init__(self):
        self._output_action = OutputAction()
        self._search_web_and_output_action = SearchWebAndOutputAction()

    def run(self, plan_list: list[Plan]) -> str:
        """
        开始执行
        :plan_list: 规划列表
        :return:
        """
        all_output = ""
        all_search_context = ""
        for plan in plan_list:
            if plan.get_type() == "search_web_and_output":
                search_context, output = self._search_web_and_output_action.search_web_and_output(
                    plan=plan, count=5
                )
                all_output += output + "\n"
                all_search_context += search_context + "\n"
            elif plan.get_type() == "output":
                output = self._output_action.output(
                    plan=plan, search_context=all_search_context
                )
                all_output += output + "\n"
        return all_output


# 用户输入
user_ask = "搜索北京今天的天气"

# 意图分析与规划
analyze_plan_list = Analyzer().analyze(query=user_ask)

# 执行工作流
answer = WorkFlow().run(plan_list=analyze_plan_list)
print(f"\n\nAnswer: {answer}")
