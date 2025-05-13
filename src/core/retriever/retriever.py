"""
@File: retriever.py
@Date: 2024/12/10 10:00
@Desc: 检索器模块
"""
from src.core.entity.search_result.result_set import ResultSet
from src.core.entity.param.retriever_param import RetrieverParam


class Retriever:
    """
    检索器
    """
    def __init__(self):
        ...

    def retrieve(self, retriever_param: RetrieverParam) -> ResultSet:
        """
        检索入口
        :return:
        """
        # 返回结果集
        return ResultSet()
