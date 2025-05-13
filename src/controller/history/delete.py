"""
@File: delete.py
@Date: 2024/12/10 10:00
@desc: 删除会话接口
"""
from flask import g
from flask_wtf import FlaskForm
from wpylib.util.http import resp_success
from wtforms.validators import DataRequired
from wtforms.fields.numeric import IntegerField
from src.api.middleware.access import access_middleware
from src.api.middleware.check_login import check_login_middleware
from src.dao.conversation import get_conversation, delete_conversation
from wpylib.middleware.validate_post_params import validate_post_params_middleware


class Form(FlaskForm):
    """
    接口表单验证
    """
    id = IntegerField("id", validators=[DataRequired()])


@access_middleware
@check_login_middleware
@validate_post_params_middleware(Form)
def search_history_delete():
    """
    主页(左侧)/删除历史会话记录按钮
    """
    # 参数处理
    context_data = g.context_data
    form_info = context_data["form_info"]
    conversation_id = form_info["id"]
    
    # 判断记录是否存在
    conversation_record = get_conversation(conversation_id=conversation_id)
    if not conversation_record:
        raise RuntimeError("记录不存在")

    # 删除记录
    delete_conversation(conversation_id=conversation_id)
    return resp_success({})
