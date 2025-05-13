"""
@File: search_web_action.py
@Date: 2024/12/10 10:00
@Desc: 联网搜索动作类
"""
from src.core.filter.filter import Filter
from src.core.filter.crawl.crawl import Crawl
from src.core.entity.search_result.result_set import ResultSet
from src.core.entity.param.retriever_param import RetrieverParam
from src.core.filter.rerank.rerank import Rerank
from src.core.filter.remove.remove import Remove
from wpylib.pkg.sse.stream_queue import StreamQueue, NoneQueue
from src.work.scheduler.action.action import Action
from src.core.retriever.bing_search_retriever import BingSearchRetriever


class SearchWebAction(Action):
    """
    联网搜索动作
    """
    _name = "search_web"
    _bing_search_retriever: BingSearchRetriever

    def __init__(self):
        super().__init__()
        self._bing_search_retriever = BingSearchRetriever()

    def do(
            self,
            search_web_param: RetrieverParam,
            filter_list: list[Filter] = None,
            queue: StreamQueue = NoneQueue(),
    ) -> ResultSet:
        """
        开始执行
        """
        # (1) 先搜索
        result_set = self._bing_search_retriever.retrieve(retriever_param=search_web_param)

        # (2) 再过滤
        for filter_instance in filter_list:
            if isinstance(filter_instance, Remove):
                result_set = filter_instance.choose(result_set)
            elif isinstance(filter_instance, Rerank):
                result_set = filter_instance.choose(result_set, top_n=3)
            elif isinstance(filter_instance, Crawl):
                result_set = filter_instance.choose(result_set)
            else:
                result_set = filter_instance.choose(result_set)

        # (3) 返回结果
        return result_set
