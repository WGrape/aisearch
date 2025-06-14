"""
@File: rerank.py
@Date: 2024/12/10 10:00
@Desc: 重排序模块
"""
from src.core.filter.filter import Filter
from src.core.entity.search_result.result_set import ResultSet
from src.core.entity.search_result.result_set_item.web_document import WebDocument
from src.core.entity.search_result.result_set_item.web_document import RESULT_SET_ITEM_TYPE_WEB_DOCUMENT


class Rerank(Filter):
    """
    重排序器
    """

    def choose(self, result_set: ResultSet, **kwargs) -> ResultSet:
        """
        筛选入口
        :return:
        """
        # 业务层重排序
        new_web_document_list: list[WebDocument] = []
        for item in result_set.get_web_document_list():
            if item.get_item_type() != RESULT_SET_ITEM_TYPE_WEB_DOCUMENT:
                continue
            new_web_document: WebDocument = item

            # 打分策略
            source = new_web_document.get_source()
            if source in ["baike.baidu.com", "baike.baidu.hk"]:
                new_web_document.add_score(10)
            elif source in ["baike.sogou.com", "zhidao.baidu.com"]:
                new_web_document.add_score(7)
            elif source in ["wenku.baidu.com", "so.gushiwen.cn", "zhihu.com"]:
                new_web_document.add_score(5)

            # 加入新的文档列表中
            new_web_document_list.append(new_web_document)

        # 对文档进行排序
        new_web_document_list = sorted(new_web_document_list, key=lambda doc: doc.get_score(), reverse=True)

        # 只获取TopN
        if "top_n" in kwargs:
            new_web_document_list = new_web_document_list[:kwargs["top_n"]]

        # 返回结果集
        result_set.reset(web_document_list=new_web_document_list)
        return result_set
