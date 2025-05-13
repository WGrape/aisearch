"""
@File: result_set_item.py
@Date: 2024/12/10 10:00
@Desc: 结果集中的条目
"""


class ResultSetItem:
    """
    结果数据集中的每个item
    """
    _item_type: str = ""
    _score: float = 0.0

    def __init__(self, item_type: str, score: float = 0.0):
        self._item_type = item_type
        self._score = score

    def add_score(self, increment: float) -> float:
        """
        增加权重值
        :param increment:
        :return:
        """
        self._score += increment
        return self._score

    def get_item_type(self) -> str:
        """
        获取item_type
        :return:
        """
        return self._item_type

    def get_score(self) -> float:
        """
        获取分数
        :return:
        """
        return self._score
