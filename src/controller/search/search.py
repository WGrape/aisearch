"""
@File: search.py
@Date: 2024/12/10 10:00
"""
from flask import Response, g
from flask_wtf import FlaskForm
from src.core.filter.crawl.crawl import Crawl
from wtforms import IntegerField, StringField
from src.core.analyzer.analyzer import Analyzer
from src.dao.reference import add_reference_list
from src.init.init import global_instance_logger
from src.core.filter.remove.remove import Remove
from src.core.filter.rerank.rerank import Rerank
from src.work.scheduler.scheduler import Scheduler
from wpylib.pkg.sse.stream_queue import StreamQueue
from src.dao.conversation import create_conversation
from src.init.init import global_instance_localcache
from wtforms.validators import DataRequired, Optional
from src.service.cache.to_answer import answer_by_cache
from src.api.middleware.access import access_middleware
from src.dao.message import get_message_list, add_message
from src.core.generator.generator import STREAM_MESSAGE_REFERENCE
from src.api.middleware.check_login import check_login_middleware
from wpylib.pkg.sse.stream_response import StreamResponseGenerator
from src.core.entity.search_result.search_result import SearchResult
from wpylib.middleware.validate_get_params import validate_get_params_middleware
from wpylib.util.http import COMMON_HTTP_CODE_PARAMS_ERROR, COMMON_HTTP_CODE_SYS_ERROR, \
    COMMON_HTTP_CODE_SUCCESS, COMMON_HTTP_CODE_MSG_MAP


class Form(FlaskForm):
    """
    接口表单验证
    """
    query = StringField("query", validators=[DataRequired()])
    mode = StringField("mode", validators=[Optional()], default="simple")
    conversation_id = IntegerField("conversation_id", validators=[Optional()], default=0)


@access_middleware
@check_login_middleware
@validate_get_params_middleware(Form)
def search_sse():
    """
    开始搜索
    """
    context_data = g.context_data
    log_id = global_instance_localcache.get_log_id()

    def process(queue: StreamQueue):
        """
        核心处理逻辑
        :param queue:
        :return:
        """
        # (1) 同步log_id
        # 由于这是一个子线程，和外部接口主线程不在同一个线程中, 所以必须在这里先同步下log_id
        global_instance_localcache.set_log_id(log_id)

        # (2) 获取请求上下文
        nonlocal context_data
        user_id = context_data["login_info"]["user_id"]

        # (3) 获取请求数据
        arg_info = context_data["arg_info"]
        query = arg_info["query"].strip()
        mode = arg_info["mode"]
        if mode not in ["simple", "professional"]:
            mode = "simple"
        conversation_id = arg_info["conversation_id"]
        if len(query) <= 0 or len(query) > 100:
            queue.send_message_end(data={
                "code": COMMON_HTTP_CODE_PARAMS_ERROR,
                "data": {"query": query},
                "msg": "提问仅限100字以内哦~"
            })
            return

        # (4) 获取当前会话的上下文
        messages = []
        if conversation_id > 0:
            messages = get_message_list(where={
                "conversation_id": conversation_id, "deleted": 0
            })
        else:
            conversation_id = create_conversation(user_id=user_id, query=query, mode=mode)

        # (5) 使用缓存回答
        if answer_by_cache(
                query=query, mode=mode, conversation_id=conversation_id, messages=messages, queue=queue
        ):
            return

        # (6) 开始重新回答
        try:
            # - 意图分析与规划
            plan = Analyzer().analysis(query=query, mode=mode, messages=messages, queue=queue)
            # - 规划的执行
            schedule_result = Scheduler().schedule(
                plan=plan,
                messages=messages,
                queue=queue,
                filter_list=[Crawl(), Remove(), Rerank()],
            )
            # - 结束
            search_result = SearchResult(
                plan=schedule_result.get_plan(),
                result_set=schedule_result.get_result_set(),
                outcome=schedule_result.get_outcome(),
            )
        except Exception as e:
            global_instance_logger.log_error("search exception", {"e": e, "query": query})
            queue.send_message_end(data={
                "code": COMMON_HTTP_CODE_SYS_ERROR,
                "msg": COMMON_HTTP_CODE_MSG_MAP[COMMON_HTTP_CODE_SYS_ERROR]
            })
            return

        # (7) 发送引用信息
        queue.send_message(type_str=STREAM_MESSAGE_REFERENCE, item={
            "list": [
                {
                    "id": doc.get_doc_index(),
                    "name": doc.get_title(),
                    "url": doc.get_url(),
                    "snippet": doc.get_description(),
                }
                for doc in search_result.get_result_set().get_web_document_list()
            ]
        })

        # (8) 会话与引用记录的保存
        # - 保存聊天对话
        message_id = add_message(
            conversation_id=conversation_id,
            query=query,
            answer=search_result.get_outcome().get_content()
        )
        # - 保存引用记录
        add_reference_list(
            conversation_id=conversation_id,
            message_id=message_id,
            crawl_id_list=search_result.get_result_set().get_crawl_id_list()
        )

        # (9) 至此，流式搜索接口响应完成，发送结束信息通知前端流程结束
        queue.send_message_end(data={
            "code": COMMON_HTTP_CODE_SUCCESS,
            "conversation_id": conversation_id,
            "message_id": message_id,
            "mode": mode,
            "answer_content": search_result.get_outcome().get_content(),
        })

    return Response(StreamResponseGenerator(process), mimetype="text/event-stream")
