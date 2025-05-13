"""
@File: knowledge_document.py
@Date: 2024/12/10 10:00
@Desc: 结果集中的知识文档类型条目
"""
from src.core.entity.search_result.result_set_item.result_set_item import ResultSetItem

RESULT_SET_ITEM_TYPE_KNOWLEDGE_DOCUMENT = "knowledge_document"


class KnowledgeDocument(ResultSetItem):
    """
    知识文档
    """
    _key: str = ""
    _value: str = ""

    def __init__(self, key: str, value: str, score: float = 0.0):
        """
        初始化
        :param key:
        :param value:
        :param score:
        """
        super().__init__(item_type=RESULT_SET_ITEM_TYPE_KNOWLEDGE_DOCUMENT, score=score)
        self._key = key
        self._value = value

    def get_key(self) -> str:
        """
        获取_key
        :return:
        """
        return self._key

    def get_value(self) -> str:
        """
        获取_value
        :return:
        """
        return self._value
