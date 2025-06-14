"""
@File: get.py
@Date: 2024/12/10 10:00
@desc: 查询会话接口
"""
from flask import g
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wpylib.util.http import resp_page_success
from wtforms.fields.numeric import IntegerField
from src.dao.crawl import get_crawl_record_list
from src.dao.reference import get_reference_list
from src.dao.conversation import get_conversation
from src.api.middleware.access import access_middleware
from src.api.middleware.check_login import check_login_middleware
from src.dao.message import get_pagination_message_list, get_message_count
from wpylib.middleware.validate_get_params import validate_get_params_middleware


class Form(FlaskForm):
    """
    接口表单验证
    """
    id = IntegerField("id", validators=[DataRequired()])
    pg = IntegerField("pg", default=1)
    pz = IntegerField("pz", default=20)


@access_middleware
@check_login_middleware
@validate_get_params_middleware(Form)
def search_history_get():
    """
    查看会话接口
    """
    # 参数处理
    context_data = g.context_data
    arg_info = context_data["arg_info"]
    conversation_id = arg_info["id"]
    pg = arg_info.get("pg", 1)
    pz = arg_info.get("pz", 20)
    if pg <= 0 or pz <= 0:
        raise RuntimeError("参数错误")

    # 获取会话记录
    conversation_record = get_conversation(conversation_id=conversation_id)

    # 获取当前页的消息列表
    messages = get_pagination_message_list(conversation_id=conversation_id, pg=pg, pz=pz)

    # 获取消息总数量
    total = get_message_count(conversation_id=conversation_id)

    # 封装结果集
    resp = []
    for message in messages:
        # 每一次对话的信息
        item = {
            "message_id": message["id"],
            "conversation_id": message["conversation_id"],
            "mode": conversation_record["mode"],
            "query": message["query"],
            "answer": message["answer"],
            "create_time": str(message["create_time"]),
            "update_time": str(message["update_time"]),
            "references": [],
        }

        # 获取网页内容记录
        reference_list = get_reference_list(message_id=message["id"], column_list=["crawl_id"])
        crawl_id_list = [reference["crawl_id"] for reference in reference_list]
        crawl_record_list = get_crawl_record_list(crawl_id_list=crawl_id_list)
        if len(crawl_record_list) <= 0:
            resp.append(item)
            continue

        # 添加references
        for crawl_record in crawl_record_list:
            item["references"].append({
                "title": crawl_record["title"],
                "description": crawl_record["description"],
                "icon": crawl_record["icon"],
                "url": crawl_record["url"],
                "source": crawl_record["source"],
                "source_name": crawl_record["source_name"],
            })
        resp.append(item)
    return resp_page_success(resp, pg, pz, total)
