"""
@File: init.py
@Date: 2024/12/10 10:00
@Desc: 服务初始化模块
"""
from wpylib.util.cmd import args_to_dict
from wpylib.util.x.xtyping import is_not_none
from wpylib.pkg.singleton.flask.flask import Flask
from wpylib.pkg.singleton.mysql.mysql import Mysql
from wpylib.pkg.singleton.logger.logger import Logger
from wpylib.pkg.singleton.milvus.milvus import Milvus
from wpylib.pkg.singleton.loader.web_loader import WebLoader
from wpylib.pkg.singleton.localcache.localcache import Localcache
from wpylib.util.storage import is_file_exist, is_directory_exist, create_directory
import yaml
import sys
import os

# 命令行参数
ARGV_INDEX_FILE: int = 0
ARGV_INDEX_ENV: int = 1
ARGV_INDEX_MODE: int = 2
ARGV_INDEX_MODE_ENTRY: int = 3

# 当前环境
ENV_DEV: str = "dev"
ENV_TEST: str = "test"
ENV_PROD: str = "prod"

# 第1次初始化: init_sysarg()
global_main_file: str = ""
global_env: str = ""
global_sys_arg_dict = {}

# 第2次初始: init_file_system()
global_base_dir: str = ""

# 第3次初始: init_config()
global_config: dict = {}

# 第4次初始化: init_instance()
global_instance_flask: Flask
global_instance_mysql: Mysql
global_instance_logger: Logger
global_instance_milvus: Milvus
global_instance_webLoader: WebLoader
global_instance_localcache: Localcache


def init_sysarg():
    """
    初始化系统参数
    """
    global global_main_file
    global global_env
    global global_sys_arg_dict

    # (1) 系统命令行参数
    global_main_file = sys.argv[ARGV_INDEX_FILE]
    global_sys_arg_dict = args_to_dict()

    # (2) 解析命令行的几个常用参数
    for arg in ["env"]:
        # 1> 依次检查不同的参数
        if arg == "env" and arg in global_sys_arg_dict:
            # --env=test
            global_env = global_sys_arg_dict[arg]
            if global_env not in [ENV_DEV, ENV_TEST, ENV_PROD]:
                print(f"sysarg env error: {global_env}")
                sys.exit(1)
    if is_not_none(os.getenv("APP_ENV")):
        global_env = os.getenv("APP_ENV")


def init_file_system():
    """
    初始化本地文件系统
    """
    # 定义需要初始化的全局变量
    global global_base_dir
    global_base_dir = os.path.abspath(os.path.join(global_main_file, "../../"))
    if "dir" in global_sys_arg_dict:
        # 防止当有意外场景导致无法获取到本项目目录的时候, 可以提供兜底的命令行--dir参数来设置当前目录
        global_base_dir = global_sys_arg_dict["dir"]
    if is_not_none(os.getenv("APP_BASE_DIR")):
        global_base_dir = os.getenv("APP_BASE_DIR")

    directory_list = [
        f"{global_base_dir}/logs",
        f"{global_base_dir}/storage",
    ]
    for directory in directory_list:
        if not is_directory_exist(directory):
            create_directory(directory)


def init_config():
    """
    初始化配置
    """
    global global_config  # 框架系统级别的配置

    # 判断配置文件是否存在
    config_file = f"{global_base_dir}/config/{global_env}/config.yml"
    if not is_file_exist(config_file):
        print(f"config file {config_file} not exists")
        sys.exit(1)

    # 配置解析, 解析/config/config.yml配置文件
    with open(config_file, "r", encoding="utf-8") as stream:
        global_config = yaml.safe_load(stream)


def init_instance():
    """
    初始化实例
    :return:
    """
    global global_config
    global global_instance_flask
    global global_instance_mysql
    global global_instance_logger
    global global_instance_milvus
    global global_instance_webLoader
    global global_instance_localcache

    global_instance_flask = Flask(app_name="flask")
    global_instance_mysql = Mysql(mysql_config=global_config["database"])
    global_instance_logger = Logger(
        logger_config=global_config["logger"], global_config=global_config
    )
    global_instance_milvus = Milvus(
        milvus_config=global_config["milvus"],
        model_config=global_config["model"]["provider"]["nomic"]
    )
    global_instance_webLoader = WebLoader()
    global_instance_localcache = Localcache()


def init_once():
    """
    初始化唯一入口
    """
    # 初始化系统参数[必须]
    init_sysarg()

    # 初始化文件系统[必须]
    init_file_system()

    # 初始化系统配置[必须]
    init_config()

    # 初始化实例对象[必须]
    init_instance()
