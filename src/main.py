"""
@File: main.py
@Date: 2024/12/10 10:00
"""
# 1. 把目录加到Python系统路径中, 防止找不到模块
import os
import sys

src_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(src_path)
for path in [src_path, root_path]:
    if path not in sys.path:
        sys.path.append(path)
print(f"sys.path: {sys.path}")

# 2. 引入服务初始化模块
from src.init.init import init_once
import traceback

try:
    init_once()
except Exception as e:
    print(traceback.format_exc())
    print(f"init_once exception: {e!r}")
    sys.exit(1)

# 3. 服务开始启动
from wpylib.util.encry import gen_random_md5
from src.init.init import global_instance_localcache

log_id = gen_random_md5()
global_instance_localcache.set_log_id(log_id)

# 4. 注册路由
from src.api.register import register as register_api

register_api()

# 5. 暴露给UWSGI
from src.init.init import global_instance_flask

app = global_instance_flask.get_instance_app()

# 6. 本地启动
# 注意：如果在服务器上运行则需要注释掉这行代码，并使用UWSGI部署
app.run(host="0.0.0.0", port="8100")
