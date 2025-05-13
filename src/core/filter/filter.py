"""
@File: filter.py
@Date: 2024/12/10 10:00
@Desc: 基类过滤器模块
"""
from src.core.entity.search_result.result_set import ResultSet


class Filter:
    """
    过滤器
    """

    def choose(self, result_set: ResultSet, **kwargs) -> ResultSet:
        """
        筛选入口
        """
        return ResultSet()
