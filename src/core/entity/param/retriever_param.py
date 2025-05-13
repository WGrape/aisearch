"""
@File: retriever_param.py
@Date: 2024/12/10 10:00
@Desc: 检索器参数
"""


class RetrieverParam:
    """
    检索器参数
    """
    _query: str = ""
    _count: int = 0
    _min_score: float = 0.0
    _start_index: int = 0

    def __init__(self, query: str, count: int = 5, min_score: float = 0.0, start_index: int = 0):
        self._query = query
        self._count = count
        self._min_score = min_score
        self._start_index = start_index

    def get_query(self) -> str:
        """
        获取查询内容
        :return:
        """
        return self._query

    def get_count(self) -> int:
        """
        获取数量
        :return:
        """
        return self._count

    def get_min_score(self) -> float:
        """
        获取最小分数
        :return:
        """
        return self._min_score

    def get_start_index(self) -> int:
        """
        获取开始下标
        :return:
        """
        return self._start_index
