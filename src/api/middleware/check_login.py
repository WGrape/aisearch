"""
@File: check_login.py
@Date: 2024/1/13 14:07
@desc: 登录检查中间件
"""
from functools import wraps
from flask import request, g
from src.init.init import global_instance_localcache


def check_login_middleware(func):
    """
    登录检查中间件
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        注解wrapper
        """

        # ...

        # 登录成功
        user = {"userId": 99}
        if "context_data" not in g:
            g.context_data = {}
        g.context_data["login_info"] = user
        g.context_data["login_info"]["user_id"] = user["userId"]
        g.context_data["login_info"]["userid"] = user["userId"]
        g.context_data["login_info"]["userId"] = user["userId"]
        global_instance_localcache.set_user_id(user["userId"])

        # 放行
        return func(*args, **kwargs)

    return wrapper
