"""
@File: remove.py
@Date: 2024/12/10 10:00
@Desc: 移除器模块
"""
from src.core.filter.filter import Filter
from src.core.entity.search_result.result_set import ResultSet
from src.core.entity.search_result.result_set_item.web_document import WebDocument
from src.core.entity.search_result.result_set_item.web_document import RESULT_SET_ITEM_TYPE_WEB_DOCUMENT


class Remove(Filter):
    """
    Remove基类
    """
    def choose(self, result_set: ResultSet, **kwargs) -> ResultSet:
        """
        筛选入口
        :return:
        """
        # 过滤不需要的数据
        new_web_document_list: list[WebDocument] = []
        web_document_list: list[WebDocument] = result_set.get_web_document_list()
        for item in web_document_list:
            if item.get_item_type() != RESULT_SET_ITEM_TYPE_WEB_DOCUMENT:
                continue
            new_web_document: WebDocument = item

            # 过滤掉的域名
            black_sources = ["baike.baidu.hk"]
            source = new_web_document.get_source()
            if source in black_sources:
                continue

            # 加入新的文档列表中
            new_web_document_list.append(new_web_document)

        # 返回结果集
        result_set.reset(web_document_list=new_web_document_list)
        return result_set
