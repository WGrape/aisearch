"""
@File: search_local_action.py
@Date: 2024/12/10 10:00
@Desc: 本地搜索动作类
"""
from src.core.entity.search_result.result_set import ResultSet
from src.core.entity.param.retriever_param import RetrieverParam
from wpylib.pkg.sse.stream_queue import StreamQueue, NoneQueue
from src.work.scheduler.action.action import Action
from src.core.retriever.milvus_search_retriever import MilvusSearchRetriever


class SearchLocalAction(Action):
    """
    本地搜索动作
    """
    _name = "search_local"
    _milvus_search_retriever: MilvusSearchRetriever

    def __init__(self):
        super().__init__()
        self._milvus_search_retriever = MilvusSearchRetriever()

    def do(
            self,
            search_local_param: RetrieverParam,
            queue: StreamQueue = NoneQueue(),
    ) -> ResultSet:
        """
        开始执行
        """
        # (1) 先搜索
        result_set = self._milvus_search_retriever.retrieve(retriever_param=search_local_param)

        # (2) 返回结果
        return result_set
