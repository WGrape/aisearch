from typing import Any


class SearchWebAction:
    """
    必应搜索类
    """
    _web_search_tool: WebSearch

    def __init__(self, engine: str, engine_config: dict):
        self._web_search_tool = WebSearch(engine=engine, engine_config=engine_config)

    def search(self, query: str, count: int) -> list:
        """
        开始搜索
        :param query: 用户输入的查询词
        :param count: 联网检索的数量
        :return:
        """
        return self._web_search_tool.search(query, count)


class LLMOutputAction:
    """
    必应搜索类
    """
    _model: Any

    def __init__(self):
        # 完成动作类的初始化
        ...

    def output(self, query: str, result_set: list) -> str:
        """
        开始搜索
        :param query: 用户输入的查询词
        :param result_set: 联网搜索结果集
        :return:
        """
        return self._model.invoke(query, result_set)


class SearchWebAndOutputAction:
    """
    必应搜索类
    """
    _search_web_action: SearchWebAction
    _llm_output_action: LLMOutputAction

    def __init__(self, engine: str, engine_config: dict):
        self._search_web_action = SearchWebAction(engine=engine, engine_config=engine_config)
        self._llm_output_action = LLMOutputAction()

    def search_and_output(self, query: str, count: int) -> (list, str):
        """
        开始搜索
        :param query: 用户输入的查询词
        :param count: 联网检索的数量
        :return:
        """
        result_set = self._search_web_action.search(query=query, count=count)
        return result_set, self._llm_output_action.output(query=query, result_set=result_set)


class WorkFlow:
    """
    工作流类
    """
    _search_web_action: SearchWebAction
    _llm_output_action: LLMOutputAction
    _search_web_and_output_action: SearchWebAndOutputAction

    def __init__(self):
        engine = "bing"
        engine_config = {}
        self._search_web_action = SearchWebAction(
            engine=engine, engine_config=engine_config
        )
        self._llm_output_action = LLMOutputAction()
        self._search_web_and_output_action = SearchWebAndOutputAction(
            engine=engine, engine_config=engine_config
        )

    def run(self, query: str, plan: list[Plan]):
        """
        开始执行
        :return:
        """
        answer = ""
        result_set_list = []
        for step in plan:
            if step.get_type() == "search_web_and_output_action":
                result_set, output = self._search_web_and_output_action.search_and_output(
                    query=query, count=5
                )
                result_set_list += result_set
                answer += output
            elif step.get_type() == "llm_output_action":
                answer += self._llm_output_action.output(query=query, result_set=result_set_list)
        return answer


def __main__():
    """
    虚拟入口
    :return:
    """

    # 用户输入的问题
    query = "唱歌的发声以及其他技巧是什么"

    # 1. 意图识别和规划
    # (1) 意图识别
    # (2) 思考规划
    # (3) 生成规划
    model = Model()
    plan = model.invoke()

    # 2. 假设得到了以下的规划数据
    plan = [
        {
            "type": "search_web_and_output_action",
            "desc": "搜索唱歌的技巧，如何发声",
            "query": "唱歌的技巧，如何发声"
        },
        {
            "type": "llm_output_action",
            "desc": "输出唱歌的技巧",
            "query": "唱歌的技巧"
        }
    ]

    # 3. 创建工作流并调用
    work_flow = WorkFlow()
    answer = work_flow.run(query=query, plan=plan)

    # 4. 输出答案
    print(answer)
