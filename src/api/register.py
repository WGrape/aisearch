"""
@File: register.py
@Date: 2024/6/13 10:20
@desc: 统一接口注册
"""
import traceback
from flask import request, jsonify
from wpylib.util.http import resp_error
from src.controller.search.search import search_sse
from src.controller.history.get import search_history_get
from src.controller.history.list import search_history_list
from src.controller.history.delete import search_history_delete
from src.controller.search.predict import predict_questions
from src.init.init import global_instance_flask, global_instance_logger


# 注册错误handler
@global_instance_flask.get_instance_app().errorhandler(Exception)
def error_handler(e):
    """
    全局异常捕获
    """
    request_base_url = request.base_url

    if request_base_url.endswith("/api") or request_base_url.endswith("/api/"):
        return jsonify({
            "data": "ok",
        })

    if request_base_url.endswith("/favicon.ico") or request_base_url.endswith("/favicon.ico/"):
        return jsonify({
            "data": "ok",
        })

    # 非根路径的请求
    global_instance_logger.log_error(
        msg="aisearch error_handler",
        biz_data={
            "exception": traceback.format_exc(),
            "exception_msg": f"{e!r}",
            "request_base_url": request_base_url,
        }
    )
    return resp_error(data={"exception": f"{e!r}"})


def register():
    """
    注册接口
    1. 注意访问地址必须和配置的路由一样, 如果最后没有配置/分隔符, 访问的时候也不要加
    """
    # 1. 获取全局flask实例
    app = global_instance_flask.get_instance_app()

    # 2. 注册接口
    app.add_url_rule(
        '/api/search/history/get', view_func=search_history_get, methods=['GET']
    )
    app.add_url_rule(
        '/api/search/history/list', view_func=search_history_list, methods=['GET']
    )
    app.add_url_rule(
        '/api/search/history/delete', view_func=search_history_delete, methods=['POST']
    )
    app.add_url_rule(
        '/api/search_sse', view_func=search_sse, methods=['GET']
    )
    app.add_url_rule(
        '/api/search/predict_questions', view_func=predict_questions, methods=['GET']
    )
