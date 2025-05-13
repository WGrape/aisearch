"""
@File: web_document.py
@Date: 2024/12/10 10:00
@Desc: 结果集中的网页文档类型条目
"""
from src.core.entity.search_result.result_set_item.result_set_item import ResultSetItem

RESULT_SET_ITEM_TYPE_WEB_DOCUMENT = "web_document"


class WebDocument(ResultSetItem):
    """
    Web资源文档
    """
    _doc_index: int = 0
    _doc_id: str = ""
    _title: str = ""
    _description: str = ""
    _icon: str = ""
    _url: str = ""
    _source: str = ""
    _source_name: str = ""
    _content: str = ""
    _hit_count: int = 0

    def __init__(
            self,
            doc_index: int,
            doc_id: str,
            title: str,
            description: str,
            icon: str = "",
            url: str = "",
            source: str = "",
            source_name: str = "",
            content: str = "",
            hit_count: int = 0,
            score: float = 0.0  # score是在内存中使用的排序字段
    ):
        super().__init__(item_type=RESULT_SET_ITEM_TYPE_WEB_DOCUMENT, score=score)
        self._doc_index = doc_index
        self._doc_id = doc_id
        self._title = title
        self._description = description
        self._icon = icon
        self._url = url
        self._source = source
        self._source_name = source_name
        self._content = content
        self._hit_count = hit_count

    def get_doc_index(self) -> int:
        """
        获取文档下标
        :return:
        """
        return self._doc_index

    def update_doc_index(self, doc_index: int):
        """
        更新文档的下标, 从1开始
        :param doc_index: 文档在结果集中的下标
        :return:
        """
        self._doc_index = doc_index

    def get_doc_id(self) -> str:
        """
        获取文档ID
        :return:
        """
        return self._doc_id

    def get_title(self) -> str:
        """
        获取标题
        :return:
        """
        return self._title

    def update_title(self, title: str):
        """
        更新标题
        :param title: 网页标题
        :return:
        """
        self._title = title

    def get_description(self) -> str:
        """
        获取描述
        :return:
        """
        return self._description

    def update_description(self, description: str):
        """
        更新描述
        :param description: 网页的简介/描述
        :return:
        """
        self._description = description

    def get_icon(self) -> str:
        """
        获取图标
        :return:
        """
        return self._icon

    def get_url(self) -> str:
        """
        获取链接
        :return:
        """
        return self._url

    def get_source(self) -> str:
        """
        获取来源
        :return:
        """
        return self._source

    def get_source_name(self) -> str:
        """
        获取来源名称
        :return:
        """
        return self._source_name

    def get_content(self) -> str:
        """
        获取内容
        :return:
        """
        return self._content

    def update_content(self, content: str):
        """
        更新内容
        :param content: 文档内容
        :return:
        """
        self._content = content

    def get_hit_count(self) -> int:
        """
        获取命中数量
        :return:
        """
        return self._hit_count

    def update_hit_count(self, hit_count: int):
        """
        更新文档的命中数量
        :param hit_count: 命中次数
        :return:
        """
        self._hit_count = hit_count

    def select_as_citation(self) -> str:
        """
        选择合适的内容作为引文
        :return:
        """
        if len(self.get_content().replace("\n", "").replace(" ", "")) < len(self.get_description()):
            return self.get_description()[:1000]

        return self.get_content()[:1000]
