"""
@File: message.py
@Date: 2024/1/29 19:41
@Desc: 消息DAO操作
"""
from src.init.init import global_instance_mysql
from wpylib.util.sql.binding import get_insert_sql, get_select_by_where_sql


def add_message(conversation_id: int, query: str, answer: str) -> int:
    """
    新增消息
    :param conversation_id: 会话ID
    :param query: 查询/提问内容
    :param answer: 答案
    :return: 返回新增消息的ID
    """
    # 生成语句
    insert_query, params = get_insert_sql(
        table="aisearch_conversation_message",
        data={
            "conversation_id": conversation_id,
            "query": query,
            "answer": answer,
        }
    )

    # 执行语句
    message_id = global_instance_mysql.execute_insert_query(
        query=insert_query,
        params=params
    )
    return message_id


def get_message_list(where: dict, limit=10) -> list:
    """
    获取消息列表
    :param where: 查询条件
    :param limit: 数量限制
    :return: 返回消息列表
    """
    # 生成语句
    select_query, params = get_select_by_where_sql(
        table="aisearch_conversation_message",
        column_list=["conversation_id", "query", "answer"],
        where=where,
        order_by="id asc",
        limit=limit,
    )

    # 执行语句
    record_list = global_instance_mysql.execute_select_query(
        query=select_query, params=params
    )

    # 封装消息
    messages = []
    for record in record_list:
        messages.append({
            "query": record["query"],
            "answer": record["answer"],
        })
    return messages


def get_pagination_message_list(conversation_id: int, pg: int, pz: int) -> list:
    """
    分页获取消息列表
    :param conversation_id: 会话ID
    :param pg: 当前页码
    :param pz: 页面容量
    :return: 分页返回当前会话的消息列表
    """
    # 生成语句
    where_str = f"where conversation_id = {conversation_id} and deleted = 0"
    order_str = "order by id asc"
    limit_str = f"limit {pz} offset {(pg - 1) * pz}"
    select_query = f"select * from aisearch_conversation_message {where_str} {order_str} {limit_str}"

    # 执行语句
    messages = global_instance_mysql.execute_select_query(query=select_query)
    return messages


def get_message_count(conversation_id: int) -> int:
    """
    获取消息总数量
    :param conversation_id: 会话ID
    :return: 返回消息总数量
    """
    # 生成语句
    where_str = "where conversation_id = %s and deleted = %s"
    select_query = f"Select count(1) as 'total' from aisearch_conversation_message {where_str}"

    # 执行语句
    total_data = global_instance_mysql.execute_select_query(
        query=select_query,
        params=[conversation_id, 0]
    )
    return total_data[0]["total"]
