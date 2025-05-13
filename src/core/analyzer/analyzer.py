"""
@File: analyzer.py
@Date: 2024/12/10 10:00
@Desc: 基类分析器模块
"""
from src.core.entity.plan.plan import Plan
from wpylib.pkg.langchain.model import Model
from src.core.entity.strategy.strategy import Strategy
from wpylib.util.x.xjson import extract_first_json
from wpylib.pkg.sse.stream_queue import StreamQueue, NoneQueue
from wpylib.pkg.langchain.history import make_conversation_history
from wpylib.pkg.langchain.prompt import create_chat_prompt_by_messages
from wpylib.pkg.langchain.chain import create_chain, make_chain_callbacks
from langchain_core.prompts.chat import SystemMessage, HumanMessagePromptTemplate
from src.init.init import global_config, global_instance_localcache, global_instance_logger
from src.core.entity.strategy.strategy import ROLE_PROFESSIONAL, EMOTION_PROFESSIONAL, ANSWER_STYLE_PROFESSIONAL

STREAM_MESSAGE_ANALYZER = "analyzer"
STREAM_MESSAGE_ANALYZER_RESULT = "analyzer_result"

DEFAULT_THOUGHT = "经过认真思考你提出的这个问题，我会利用我的理解和学习能力，给你提供最准确的答案。"
DEFAULT_INTENTION_PLAN = {
    "plan": [],
    "intention": "none",
    "thought": DEFAULT_THOUGHT
}
INTENTION_TYPE_METHOD: str = "method"
INTENTION_TYPE_SUMMARY: str = "summary"
INTENTION_TYPE_WRITE: str = "write"
INTENTION_TYPE_NONE: str = "none"
INTENTION_LIST = [
    INTENTION_TYPE_METHOD,
    INTENTION_TYPE_SUMMARY,
    INTENTION_TYPE_WRITE,
    INTENTION_TYPE_NONE,
]
ACTION_TYPE_END: str = "end"
ACTION_TYPE_OUTPUT: str = "output"
ACTION_TYPE_SEARCH_WEB: str = "search_web"
ACTION_TYPE_SEARCH_LOCAL: str = "search_local"
ACTION_TYPE_SEARCH_WEB_AND_OUTPUT: str = "search_web_and_output"
ACTION_TYPE_SEARCH_LOCAL_AND_OUTPUT: str = "search_local_and_output"
ACTION_TYPE_LIST = [
    ACTION_TYPE_END,
    ACTION_TYPE_OUTPUT,
    ACTION_TYPE_SEARCH_WEB,
    ACTION_TYPE_SEARCH_LOCAL,
    ACTION_TYPE_SEARCH_WEB_AND_OUTPUT,
    ACTION_TYPE_SEARCH_LOCAL_AND_OUTPUT
]


class Analyzer:
    """
    意图分析器
    """
    # 定义所需要的问题分类、查询改写、意图识别与规划的系统提示词
    _analysis_category_system_prompt = f"""
# 问题分类器
你是一个问题分类器，可以识别用户的问题属于什么类目
## Context
- 自然科学与工程：如物理与天文、化学与材料、生命科学与环境、计算机与信息技术
- 数学与思维逻辑：如基础数学、初等数学、高等数学
- 创作与人文历史：文学与创作、语言学与交流、历史与文化、哲学与思想、艺术与审美
- 社会与人类科学：政治与法律、经济与管理、社会学与人类学、心理学与行为科学、医学
- 生活与实用技能：教育与学习、生活与健康、运动与休闲、职业与创业
- 影视资讯与讨论：电影分享、电影推荐、电影信息、电影观看
- 交流与日常互动：日常对话
## Constrains
1. 返回结构如下所示
```json
{{
"category": ""
}}
```
## Workflow
1. 认真理解用户输入的内容先判断用户是在和你打招呼，和你简单的聊天，还是在向你提问
2. 从<Context>中选择一个或多个合适的类目，标记此用户的问题的所属类目
3. 按要求返回结果
"""
    _analysis_rewriting_system_prompt = f"""
# 角色
query改写器
## 示例
### 示例一
输入：李白
输出：
```json
{{
"query_list": ["李白"],
}}
```
输入：他是谁
输出：
```json
{{
"query_list": ["李白是谁"],
}}
```
### 示例二
输入：求鞋推荐
输出：
```json
{{
"query_list": ["球鞋推荐"],
}}
```
## 要求
1. 不要扩展提问的含义。
## 工作流
1. 认真理解聊天记录
2. 先判断用户的提问是否存在指代。
3. 如果存在指代，则你需要根据上下文，完成指代消解。
4. 再判断用户的提问是否存在省略（表达不完整、不清晰）。
5. 如果存在省略，则你需要根据上下文，完成省略补全。
6. 把修改后的一个或多个用户Query，按要求的结构返回
## 任务
你需要对用户的Query做指代消解及省略补全
"""
    _analysis_intention_system_prompt = f"""
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
- 本地检索并输出:  {{"type": "search_local_and_output", "keyword": "the search keyword", "part": "which part does the output belong to"}}
- 仅输出:  {{"type": "output", "part": "which part does the output belong to"}}
- 结束:  {{"type": "end"}}
## 示例
### 请介绍《英雄儿女》这部电影
```json
{{
    "thought": "嗯，你想要《英雄儿女》这部电影的介绍，我需要从多个角度进行。首先，由于这是一部电影，所以，我会进行本地检索并输出关于《喜剧之王》的基本信息和背景。接着，我会联网搜索并输出这部电影的主题和情节分析。然后，我会联网搜索并输出这部电影的历史意义。最后，我会总结这些信息，给出一个全面的介绍。",
    "plan": [
        {{"type": "search_local_and_output", "keyword": "英雄儿女的基本信息", "part": "基本信息"}},
        {{"type": "search_web_and_output", "keyword": "英雄儿女的主题和情节分析", "part": "主题和情节"}},
        {{"type": "search_web_and_output", "keyword": "英雄儿女的历史意义", "part": "历史意义"}},
        {{"type": "output", "part": "总结"}},
        {{"type": "end"}}
    ],
    "intention": "summary"
}}
```
## 要求
1. 如果提问意图为”method“，必须按照有顺序、有逻辑条理的方式来解答。
2. 如果提问意图为”summary“，则必须在正面回答问题的前提下，自行规划。
3. 如果涉及到和电影信息相关的步骤，你必须调用search_local_and_output本地搜索动作。
"""

    def _make_user_prompt(self, query: str, messages: list = None):
        """
        生成user部分prompt
        :param query:
        :param messages:
        :return:
        """
        user_prompt = f"{make_conversation_history(messages)}\n\n## 用户提问\n{query}"
        return user_prompt

    def analysis_category(self, query: str, messages: list = None) -> dict:
        """
        分析问题类目
        """
        # 拼接用户部分的Prompt
        user_prompt = self._make_user_prompt(query=query, messages=messages)

        # 初始化LLMChain实例
        model_config = global_config["model"]["provider"]["deepseek_chat"]
        model = Model(model_type=model_config["model_type"], model_config=model_config)
        prompt = create_chat_prompt_by_messages(messages=[
            SystemMessage(content=self._analysis_category_system_prompt),
            HumanMessagePromptTemplate.from_template("{input}"),
        ])
        chain = create_chain(
            model=model.get_raw_model(),
            prompt=prompt,
        )
        llm_invoke = chain.invoke(
            input=user_prompt,
            config={
                "callbacks": make_chain_callbacks(
                    langfuse_config=global_config["langfuse"],
                    log_id=global_instance_localcache.get_log_id()
                )
            }
        )

        # 解析大模型的返回
        llm_result = extract_first_json(llm_invoke["text"])

        # 检查大模型的返回
        category_list = [
            "自然科学与工程",
            "数学与思维逻辑",
            "创作与人文历史",
            "社会与人类科学",
            "生活与实用技能",
            "影视资讯与讨论",
            "交流与日常互动"
        ]
        if "category" not in llm_result or not isinstance(llm_result["category"], str) \
                or llm_result["category"] not in category_list:
            llm_result["category"] = "交流与日常互动"
        return llm_result

    def analysis_rewriting(self, query: str, messages: list = None) -> dict:
        """
        用户query改写
        :return:
        """
        # 如果超过一定长度, 则不做Query改写
        max_len = 30
        if len(query) > max_len:
            return {"query_list": [query]}

        # 拼接用户部分的Prompt
        user_prompt = self._make_user_prompt(query=query, messages=messages)

        # 初始化LLMChain实例
        model_config = global_config["model"]["provider"]["deepseek_chat"]
        model = Model(model_type=model_config["model_type"], model_config=model_config)
        prompt = create_chat_prompt_by_messages(messages=[
            SystemMessage(content=self._analysis_rewriting_system_prompt),
            HumanMessagePromptTemplate.from_template("{input}"),
        ])
        chain = create_chain(
            model=model.get_raw_model(),
            prompt=prompt,
        )
        llm_invoke = chain.invoke(
            input=user_prompt,
            config={
                "callbacks": make_chain_callbacks(
                    langfuse_config=global_config["langfuse"],
                    log_id=global_instance_localcache.get_log_id()
                )
            }
        )

        # 解析大模型的返回
        llm_result = extract_first_json(llm_invoke["text"])
        return llm_result

    def analysis_intention_plan(
            self, query: str, messages: list = None, queue: StreamQueue = NoneQueue()
    ):
        """
        分析意图识别并规划
        :return:
        """
        # 创建模型
        user_prompt = self._make_user_prompt(query=query, messages=messages)
        model_config = global_config["model"]["provider"]["deepseek_chat"]
        model = Model(model_type=model_config["model_type"], model_config=model_config)
        prompt = create_chat_prompt_by_messages(messages=[
            SystemMessage(content=self._analysis_intention_system_prompt),
            HumanMessagePromptTemplate.from_template("{input}"),
        ])
        chain = create_chain(
            model=model.get_raw_model(),
            prompt=prompt,
        )

        # 调用并解析大模型的返回
        llm_invoke = chain.invoke(
            input=user_prompt,
            config={
                "callbacks": make_chain_callbacks(
                    langfuse_config=global_config["langfuse"],
                    log_id=global_instance_localcache.get_log_id()
                )
            }
        )
        try:
            # 上下文太长，会偶现输出错误，需要兼容处理
            llm_result = extract_first_json(llm_invoke["text"])
        except Exception as e:
            global_instance_logger.log_error(msg="json error", biz_data={"e": e})
            return DEFAULT_INTENTION_PLAN

        # 检查大模型返回
        # (1) thought 字段检查
        if "thought" not in llm_result or llm_result["thought"] == "":
            llm_result["thought"] = DEFAULT_THOUGHT
        # (2) plan/intention 字段检查
        if "plan" not in llm_result or not isinstance(llm_result["plan"], list) \
                or "intention" not in llm_result or llm_result["intention"] not in INTENTION_LIST:
            queue.send_message(
                type_str=STREAM_MESSAGE_ANALYZER_RESULT,
                item={"result": llm_result, "content": f"正在意图识别与规划中，已自动切换为简单意图。"}
            )
            return DEFAULT_INTENTION_PLAN
        # (3) 检查plan中每个动作是否正确
        new_action_list = []
        for index, item in enumerate(llm_result["plan"]):
            # 检查type字段
            if "type" not in item or item["type"] not in ACTION_TYPE_LIST:
                continue
            # 检查output类型
            if item["type"] == ACTION_TYPE_OUTPUT and "part" not in item:
                continue
            # 检查search_web_and_output类型
            if item["type"] == ACTION_TYPE_SEARCH_WEB_AND_OUTPUT and "part" not in item and "keyword" not in item:
                continue
            # 检查search_local_and_output类型
            if item["type"] == ACTION_TYPE_SEARCH_LOCAL_AND_OUTPUT and "part" not in item and "keyword" not in item:
                continue
            if "part" not in item and "keyword" in item:
                item["part"] = item["keyword"]
            new_action_list.append(item)
        # (4) 如果没有动作列表为空, 则返回默认规划
        if len(new_action_list) <= 0:
            queue.send_message(
                type_str=STREAM_MESSAGE_ANALYZER_RESULT,
                item={"result": llm_result, "content": f"正在意图识别与规划中，已自动切换为简单意图。"}
            )
            return DEFAULT_INTENTION_PLAN
        # (5) 如果无意图, 则直接返回对应的规划
        if llm_result["intention"] == INTENTION_TYPE_NONE:
            queue.send_message(
                type_str=STREAM_MESSAGE_ANALYZER_RESULT,
                item={"result": llm_result, "content": f"正在意图识别与规划中，已识别为简单意图。"}
            )
            return llm_result
        llm_result["plan"] = new_action_list

        # 返回结果
        queue.send_message(
            type_str=STREAM_MESSAGE_ANALYZER_RESULT,
            item={"result": llm_result, "content": f"正在意图识别与规划中，生成的规划如下：{llm_result['thought']}"}
        )
        return llm_result

    def analysis(self, query: str, mode: str, messages: list = None, queue: StreamQueue = NoneQueue()) -> Plan:
        """
        开始分析
        :param query: 查询
        :param mode: 模式
        :param messages: 消息列表
        :param queue: 队列
        :return:
        """
        # 意图识别与规划
        llm_result = self.analysis_intention_plan(query=query, messages=messages, queue=queue)

        # 角色与回答模板机制
        strategy = Strategy()
        if mode == "professional":
            strategy = Strategy(
                role=ROLE_PROFESSIONAL, emotion=EMOTION_PROFESSIONAL, answer_style=ANSWER_STYLE_PROFESSIONAL
            )

        # 返回规划结果
        plan = Plan(
            query=query,
            query_rewriting=self.analysis_rewriting(query=query, messages=messages),
            query_domain=self.analysis_category(query=query, messages=messages),
            strategy=strategy,
            user_prompt=f"""
{make_conversation_history(messages)}
## 用户提问
{query}
## 要求
1. 必须输出标题“## {{title}}”"
            """,
            # 这个类(Plan的子类)的自定义需要的参数
            action_list=llm_result["plan"],
            intention=llm_result["intention"],
        )
        return plan
