"""
@File: action.py
@Date: 2024/12/10 10:00
@Desc: 动作基类模块
"""
from typing import Any


class Action:
    """
    动作
    """
    _action_name = "action"

    def __init__(self):
        pass

    def do(
            self,
            **kwargs
    ) -> Any:
        """
        开始执行
        """
        ...
