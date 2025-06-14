"""
@File: crawl.py
@Date: 2024/12/10 10:00
@desc: 网页内容DAO操作
"""
from typing import Tuple
from src.init.init import global_instance_mysql
from src.core.entity.search_result.result_set_item.web_document import WebDocument
from wpylib.util.sql.binding import get_select_by_where_sql, get_insert_or_update_sql
import copy


def add_crawl_record_list(web_document_list: list[WebDocument] = None) -> list[int]:
    """
    新增网页内容记录
    :param web_document_list: Web文档列表
    :return: 返回新增的ID列表
    """
    insert_id_list: list[int] = []

    for web_document in web_document_list:
        # 封装插入数据
        insert_data = {
            "doc_id": web_document.get_doc_id(),
            # 网页基本信息
            "title": web_document.get_title(),
            "url": web_document.get_url(),
            "description": web_document.get_description(),
            "icon": web_document.get_icon(),
            "source": web_document.get_source(),
            "source_name": web_document.get_source_name(),
            "content": web_document.get_content(),
        }

        # 封装更新数据(在Python中，可以使用对象的深拷贝来防止数据污染)
        update_data = copy.deepcopy(insert_data)
        update_data["hit_count +"] = "1"

        # 生成语句
        insert_or_update_query, params = get_insert_or_update_sql(
            table="aisearch_crawl",
            data=insert_data,
            update_data=update_data
        )

        # 执行语句
        insert_id = global_instance_mysql.execute_insert_or_update_query(
            query=insert_or_update_query,
            params=params
        )
        insert_id_list.append(insert_id)

    return insert_id_list


def get_crawl_record(doc_id: str) -> Tuple[bool, dict]:
    """
    获取网页内容记录
    :param doc_id: 文档ID
    :return:
    """
    # 生成语句
    select_query, params = get_select_by_where_sql(
        table="aisearch_crawl",
        column_list=["*"],
        where={
            "doc_id": doc_id,
        },
        order_by="id desc",
        limit=1
    )

    # 执行语句
    record_list = global_instance_mysql.execute_select_query(
        query=select_query,
        params=params
    )
    if len(record_list) > 0:
        return True, record_list[0]
    return False, {}


def get_crawl_record_list(crawl_id_list: list[str]) -> list:
    """
    获取网页内容记录列表
    :return:crawl_id_list
    """
    if len(crawl_id_list) <= 0:
        return []

    # 生成语句
    select_query, params = get_select_by_where_sql(
        table="aisearch_crawl",
        column_list=["*"],
        where={
            "id": crawl_id_list,
        },
        order_by="id asc",
    )

    # 执行语句
    record_list = global_instance_mysql.execute_select_query(
        query=select_query,
        params=params
    )
    return record_list
