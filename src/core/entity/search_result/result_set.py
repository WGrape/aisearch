"""
@File: result_set.py
@Date: 2024/12/10 10:00
@Desc: 结果集
"""
from wpylib.util.encry import sha1
from wpylib.util.x.xtyping import is_not_none
from src.core.entity.search_result.result_set_item.web_document import WebDocument
from src.core.entity.search_result.result_set_item.knowledge_document import KnowledgeDocument


class ResultSet:
    """
    结果集对象
    """
    # 输入
    _web_document_list: list[WebDocument] = []
    _knowledge_document_list: list[KnowledgeDocument] = []
    _crawl_id_list: list[int] = []
    _extra_data: dict = {}

    # 输出
    _reference_list: list[dict] = []

    @staticmethod
    def combine(result_set_list: list['ResultSet']) -> 'ResultSet':
        """
        合并
        :param result_set_list: 结果集列表
        :return:
        """
        combine_extra_data: dict = {}
        combine_crawl_id_list: list[int] = []
        combine_web_document_list: list[WebDocument] = []
        for temp_result_set in result_set_list:
            combine_extra_data.update(temp_result_set.get_extra_data())
            combine_crawl_id_list.extend(temp_result_set.get_crawl_id_list())
            combine_web_document_list.extend(temp_result_set.get_web_document_list())

        combine_result_set = ResultSet()
        combine_result_set.reset(
            web_document_list=combine_web_document_list,
            crawl_id_list=combine_crawl_id_list,
            extra_data=combine_extra_data,
        )
        return combine_result_set

    def reset(
            self,
            web_document_list: list[WebDocument] = None,
            knowledge_document_list: list[KnowledgeDocument] = None,
            crawl_id_list: list[int] = None,
            extra_data: dict = None
    ):
        """
        重置result_set
        :param: web_document_list web文档列表
        :param: knowledge_document_list 知识文档列表
        :param: crawl_id_list: crawl_id列表
        :param: extra_data: 额外数据
        :return:
        """
        if is_not_none(web_document_list):
            for index, v in enumerate(web_document_list):
                web_document_list[index].update_doc_index(index + 1)

            self._web_document_list = web_document_list
            self._web_document_list = sorted(self._web_document_list, key=lambda doc: doc.get_score(), reverse=True)

            # 一定要重置数据, 否则在reset的时候数据会多次append
            self._reference_list = []
            for web_document in self._web_document_list:
                self._reference_list.append({
                    "doc_index": web_document.get_doc_index(),
                    "doc_id": sha1(web_document.get_url()),
                    "title": web_document.get_title(),
                    "url": web_document.get_url(),
                })

        if is_not_none(knowledge_document_list):
            self._knowledge_document_list = knowledge_document_list
        if is_not_none(crawl_id_list):
            self._crawl_id_list = crawl_id_list
        if is_not_none(extra_data):
            self._extra_data = extra_data

    def get_web_document_list(self) -> list[WebDocument]:
        """
        获取网页文档结果集: 自动按照score排序
        :return:
        """
        return self._web_document_list

    def get_knowledge_document_list(self) -> list[KnowledgeDocument]:
        """
        获取知识库文档结果集
        :return:
        """
        return self._knowledge_document_list

    def get_reference_list(self) -> list[dict]:
        """
        获取引用列表
        :return:
        """
        return self._reference_list

    def get_crawl_id_list(self) -> list[int]:
        """
        获取crawl_id列表
        :return:
        """
        return self._crawl_id_list

    def get_extra_data(self) -> dict:
        """
        获取_extra_data
        :return:
        """
        return self._extra_data
