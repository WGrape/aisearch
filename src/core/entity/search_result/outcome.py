"""
@File: outcome.py
@Date: 2024/12/10 10:00
@Desc: 结果内容部分
"""
OUTCOME_TYPE_MARKDOWN = "markdown"
OUTCOME_TYPE_MINDMAP = "mindmap"


class Outcome:
    """
    通用返回结果内容
    """
    _content: str
    _content_type: str

    def __init__(self, content: str, content_type: str = OUTCOME_TYPE_MARKDOWN):
        self._content = content
        self._content_type = content_type

    @staticmethod
    def combine(outcome_list: list['Outcome'], join_char: str = "\n") -> 'Outcome':
        """
        合并Outcome
        :param outcome_list: outcome结果内容列表
        :param join_char: 连接符
        :return:
        """
        content_list: list[str] = []
        for temp_outcome in outcome_list:
            content_list.append(temp_outcome.get_content())

        return Outcome(content=join_char.join(content_list))

    def get_content(self) -> str:
        """
        获取内容
        :return:
        """
        return self._content

    def get_content_type(self) -> str:
        """
        获取content_type
        :return:
        """
        return self._content_type
