"""
@File: predict.py
@Date: 2024/12/10 10:00
@desc: 预测问题接口
"""
from flask import g
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import Optional
from wpylib.util.http import resp_success
from src.api.middleware.access import access_middleware
from src.service.predict.predict import gen_predict_questions
from src.api.middleware.check_login import check_login_middleware
from wpylib.middleware.validate_get_params import validate_get_params_middleware


class Form(FlaskForm):
    """
    接口表单验证
    """
    conversation_id = IntegerField("conversation_id", validators=[Optional()], default=0)


@access_middleware
@check_login_middleware
@validate_get_params_middleware(Form)
def predict_questions():
    """
    搜索
    """
    # 获取上下文数据
    context_data = g.context_data

    # 获取请求数据
    arg_info = context_data["arg_info"]
    conversation_id = arg_info["conversation_id"]
    if conversation_id < 1:
        # 结果响应
        return resp_success({
            "questions": []
        })

    # 生成预测问题
    gen_questions = gen_predict_questions(conversation_id=conversation_id)

    # 封装问题列表
    question_list = []
    for index, item in enumerate(gen_questions):
        question_list.append({
            "question": item,
            "id": index + 1
        })

    # 结果响应
    return resp_success({
        "questions": question_list
    })
