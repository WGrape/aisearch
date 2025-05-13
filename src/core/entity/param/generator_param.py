"""
@File: generator_param.py
@Date: 2024/12/10 10:00
@Desc: 生成器参数
"""
from src.core.entity.strategy.strategy import Strategy


class GeneratorParam:
    """
    生成器参数
    """
    _query: str
    _query_rewriting: dict
    _query_domain: dict
    _strategy: Strategy
    _user_prompt: str

    _param_type: str = ""

    def __init__(
            self,
            query: str,
            query_rewriting: dict,
            query_domain: dict,
            strategy: Strategy,
            user_prompt: str,
            param_type: str = ""
    ):
        self._query = query
        self._query_rewriting = query_rewriting
        self._query_domain = query_domain
        self._strategy = strategy
        self._user_prompt = user_prompt

        self._param_type = param_type

    def get_query(self) -> str:
        """
        返回_query
        :return:
        """
        return self._query

    def get_query_rewriting(self) -> dict:
        """
        返回_query_rewriting
        :return:
        """
        return self._query_rewriting

    def get_query_domain(self) -> dict:
        """
        返回_query_domain
        :return:
        """
        return self._query_domain

    def get_strategy(self) -> Strategy:
        """
        返回_strategy
        :return:
        """
        return self._strategy

    def get_user_prompt(self) -> str:
        """
        返回_user_prompt
        :return:
        """
        return self._user_prompt

    def get_param_type(self) -> str:
        """
        返回参数类型
        :return:
        """
        return self._param_type
