"""
@File: search_local_and_output_action.py
@Date: 2024/12/10 10:00
@Desc: 本地搜索并输出动作类
"""
from src.core.entity.search_result.outcome import Outcome
from src.core.entity.search_result.result_set import ResultSet
from src.core.entity.param.generator_param import GeneratorParam
from src.core.entity.param.retriever_param import RetrieverParam
from wpylib.pkg.sse.stream_queue import StreamQueue, NoneQueue
from src.work.scheduler.action.action import Action
from src.work.scheduler.action.output_action import OutputAction
from src.work.scheduler.action.search_local_action import SearchLocalAction


class SearchLocalAndOutputAction(Action):
    """
    动作: 本地搜索且输出
    """
    # 基础属性
    _name = "search_local_and_output"
    _search_action: SearchLocalAction
    _output_action: OutputAction

    def __init__(self):
        super().__init__()
        self._search_action = SearchLocalAction()
        self._output_action = OutputAction()

    def do(
            self,
            search_local_param: RetrieverParam,
            generator_param: GeneratorParam,
            messages: list = None,
            queue: StreamQueue = NoneQueue(),
    ) -> (ResultSet, Outcome):
        """
        开始执行
        """
        # (1) 先搜索
        result_set = self._search_action.do(
            search_local_param=search_local_param,
            queue=queue
        )
        # (2) 再调用生成
        outcome = self._output_action.do(
            generator_param=generator_param,
            result_set=result_set,
            messages=messages,
            queue=queue
        )
        # (3) 返回结果
        return result_set, outcome
