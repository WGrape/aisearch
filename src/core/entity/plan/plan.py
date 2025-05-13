"""
@File: plan.py
@Date: 2024/12/10 10:00
@Desc: 规划类
"""
from src.core.entity.strategy.strategy import Strategy


class Plan:
    """
    规划
    """
    _query: str = ""
    _query_rewriting: dict
    _query_domain: dict
    _strategy: Strategy
    _user_prompt: str = ""

    _intention: str
    _action_list: list[dict]

    def __init__(
            self,
            # 通用型参数
            query: str,
            query_rewriting: dict,
            query_domain: dict,
            strategy: Strategy,
            user_prompt: str,
            intention: str,
            action_list: list[dict],
    ):
        self._query = query
        self._query_rewriting = query_rewriting
        self._query_domain = query_domain
        self._strategy = strategy
        self._user_prompt = user_prompt

        self._intention = intention
        self._action_list = action_list

    def get_query(self) -> str:
        """
        获取query
        :return:
        """
        return self._query

    def get_query_rewriting(self) -> dict:
        """
        获取query_rewriting
        :return:
        """
        return self._query_rewriting

    def get_query_domain(self) -> dict:
        """
        获取query_domain
        :return:
        """
        return self._query_domain

    def get_strategy(self) -> Strategy:
        """
        获取strategy
        :return:
        """
        return self._strategy

    def get_user_prompt(self) -> str:
        """
        获取user_prompt
        :return:
        """
        return self._user_prompt

    def get_intention(self) -> str:
        """
        获取intention
        :return:
        """
        return self._intention

    def get_action_list(self) -> list[dict]:
        """
        获取action_list
        :return:
        """
        return self._action_list
