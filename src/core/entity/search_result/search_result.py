"""
@File: search_result.py
@Date: 2024/12/10 10:00
@Desc: 搜索结果
"""
from src.core.entity.plan.plan import Plan
from src.core.entity.search_result.outcome import Outcome
from src.core.entity.search_result.result_set import ResultSet


class SearchResult:
    """
    搜索结果
    """
    # 结果相关
    _plan: Plan  # 规划：分析阶段的产物
    _result_set: ResultSet  # 数据集: 检索阶段的产物
    _outcome: Outcome  # 结果: 生成阶段的产物

    def __init__(
            self,
            plan: Plan,
            result_set: ResultSet,
            outcome: Outcome,
    ):
        self._plan = plan
        self._result_set = result_set
        self._outcome = outcome

    def get_plan(self) -> Plan:
        """
        获取plan
        :return:
        """
        return self._plan

    def get_result_set(self) -> ResultSet:
        """
        获取搜索结果集
        :return:
        """
        return self._result_set

    def get_outcome(self) -> Outcome:
        """
        获取总结结果
        :return:
        """
        return self._outcome
