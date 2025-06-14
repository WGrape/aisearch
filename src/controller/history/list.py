"""
@File: list.py
@Date: 2024/12/10 10:00
@desc: 会话记录列表接口
"""
from flask import g
from flask_wtf import FlaskForm
from wpylib.util.http import resp_page_success
from wtforms.fields.numeric import IntegerField
from src.api.middleware.access import access_middleware
from src.api.middleware.check_login import check_login_middleware
from wpylib.middleware.validate_get_params import validate_get_params_middleware
from src.dao.conversation import get_conversation_count, get_pagination_conversation_list


class Form(FlaskForm):
    """
    接口表单验证
    """
    pg = IntegerField("pg", default=1)
    pz = IntegerField("pz", default=20)


@access_middleware
@check_login_middleware
@validate_get_params_middleware(Form)
def search_history_list():
    """
    会话记录列表
    """
    context_data = g.context_data
    arg_info = context_data["arg_info"]
    pg = arg_info.get("pg", 1)
    pz = arg_info.get("pz", 20)
    if pg <= 0 or pz <= 0:
        raise RuntimeError("参数错误")
    user = context_data["login_info"]
    user_id = user["user_id"]

    # 获取会话总数量
    total = get_conversation_count(user_id=user_id)

    # 分页获取会话
    conversations = get_pagination_conversation_list(user_id=user_id, pg=pg, pz=pz)
    if not conversations:
        return resp_page_success([], pg, pz, total)

    # 封装返回结果
    for index, item in enumerate(conversations):
        conversations[index]["create_time"] = str(conversations[index]["create_time"])
        conversations[index]["update_time"] = str(conversations[index]["update_time"])
    return resp_page_success(conversations, pg, pz, total)
