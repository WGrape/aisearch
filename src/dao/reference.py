"""
@File: reference.py
@Date: 2024/1/29 19:41
@Desc: 引用DAO操作
"""
from src.init.init import global_instance_mysql
from wpylib.util.sql.binding import get_insert_sql, get_select_by_where_sql


def add_reference_list(
        conversation_id: int,
        message_id: int,
        crawl_id_list: list[int]
):
    """
    新增引用列表
    :param conversation_id: 会话ID
    :param message_id: 消息ID
    :param crawl_id_list: crawl_id列表
    :return:
    """
    for crawl_id in crawl_id_list:
        # 生成语句
        insert_query, params = get_insert_sql(
            table="aisearch_conversation_reference",
            data={
                "conversation_id": conversation_id,
                "message_id": message_id,
                "crawl_id": crawl_id,
            }
        )

        # 执行语句
        global_instance_mysql.execute_insert_query(
            query=insert_query,
            params=params
        )


def get_reference_list(message_id: int, column_list: list) -> list:
    """
    获取引用列表
    :param message_id: 消息ID
    :param column_list: 字段列表
    :return: 获取引用列表
    """
    # 生成语句
    select_query, params = get_select_by_where_sql(
        table="aisearch_conversation_reference",
        column_list=column_list,
        where={
            "message_id": message_id,
            "deleted": 0,
        },
        order_by="id"
    )

    # 执行语句
    references = global_instance_mysql.execute_select_query(
        query=select_query,
        params=params
    )
    return references
