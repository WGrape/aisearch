"""
@File: conversation.py
@Date: 2024/1/29 19:41
@Desc: 会话DAO操作
"""
from src.init.init import global_instance_mysql
from wpylib.util.sql.binding import get_insert_sql, get_update_sql, get_select_by_where_sql


def create_conversation(user_id: int, query: str, mode: str = "simple") -> int:
    """
    创建会话
    :param user_id: 用户ID
    :param query: 查询内容
    :param mode: 问答模式
    :return: 返回创建的会话ID
    """
    # 生成语句
    insert_query, params = get_insert_sql(
        table="aisearch_conversation",
        data={
            "user_id": user_id,
            "query": query,
            "mode": mode
        }
    )

    # 执行语句
    conversation_id = global_instance_mysql.execute_insert_query(
        query=insert_query,
        params=params
    )
    return conversation_id


def get_conversation(conversation_id: int) -> dict | None:
    """
    获取会话
    :param conversation_id: 会话ID
    :return: 返回会话
    """
    # 生成语句
    select_query, params = get_select_by_where_sql(
        table="aisearch_conversation",
        column_list=["*"],
        where={
            "id": conversation_id
        }
    )

    # 执行语句
    conversation_list = global_instance_mysql.execute_select_query(
        query=select_query,
        params=params
    )
    if len(conversation_list) <= 0:
        return None
    return conversation_list[0]


def delete_conversation(conversation_id: int):
    """
    删除会话
    :param conversation_id: 会话ID
    """
    # 生成语句
    update_query, params = get_update_sql(
        table="aisearch_conversation",
        data={
            "deleted": 1,
        },
        where={
            "id": conversation_id
        }
    )

    # 执行语句
    global_instance_mysql.execute_update_query(
        query=update_query,
        params=params
    )


def get_pagination_conversation_list(user_id: int, pg: int, pz: int) -> list:
    """
    分页获取会话列表
    :param user_id: 用户ID
    :param pg: 当前页码
    :param pz: 每页容量
    :return: 分页获取会话
    """
    # 生成语句
    where_str = f"where user_id = {user_id}"
    order_str = "order by id desc"
    limit_str = f"limit {pz} offset {(pg - 1) * pz}"
    select_query = f"select * from aisearch_conversation {where_str} {order_str} {limit_str}"

    # 执行语句
    conversations = global_instance_mysql.execute_select_query(query=select_query)
    return conversations


def get_conversation_count(user_id: int) -> int:
    """
    获取会话总数量
    :param user_id: 用户ID
    :return: 返回会话总数量
    """
    # 生成语句
    where_str = f"where user_id = {user_id}"
    select_query = f"select count(1) as 'total' from aisearch_conversation {where_str}"

    # 执行语句
    total_data = global_instance_mysql.execute_select_query(query=select_query)
    if len(total_data) <= 0:
        return 0
    return total_data[0]["total"]
