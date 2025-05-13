"""
@File: to_answer.py
@Date: 2024/1/29 19:41
@Desc: 使用缓存回答的逻辑
"""
from src.dao.message import add_message
from wpylib.pkg.langchain.model import Model
from wpylib.util.http import COMMON_HTTP_CODE_SUCCESS
from wpylib.pkg.langchain.chain import make_chain_callbacks
from wpylib.pkg.sse.stream_queue import StreamQueue, NoneQueue
from langchain_core.prompts.chat import SystemMessage, HumanMessage
from src.core.analyzer.analyzer import Analyzer, STREAM_MESSAGE_ANALYZER_RESULT
from src.core.generator.generator import STREAM_MESSAGE_GENERATION, STREAM_MESSAGE_GENERATION_PENDING
from src.init.init import global_config, global_instance_logger, global_instance_localcache, global_instance_milvus

system_prompt_template = """
# Role
你是一个智能回答助手
## Context
{answer_from_cache}
## Constrains
- 禁止对用户的问题不作答，即使<Context>中无可参考的信息，也必须根据你自己的能力回答
- 您的回答必须正确、准确，并由专家使用无偏见且专业的语气撰写。
- 禁止在回答中说你参考了<Context>中的信息。
- 请不要在回答中提供与问题无关的信息，也不要重复。
- 请从始至终使用中文回答。
## Workflow
1. 先认真分析用户输入的问题
2. 判断<Context>内容是否可以作为回答问题时的参考
3. 如果<Context>内容与问题毫无关系，则自行回答即可
4. 如果<Context>内容中部分与问题有关，则参考<Context>中相关的内容，回答用户的问题
## Goal
结合<Context>内容，回答用户的问题
"""

user_prompt_template = """
## 要求
1、必须基于<Context>中的答案，按照原格式返回。
2、允许多样性处理，比如在不改变原意下某些句式、词汇的调整等。
3、**禁止**输出“答案“。

## 用户问题
{query}
"""


def answer_by_cache(
        query: str,
        mode: str,
        conversation_id: int,
        messages: list = None,
        queue: StreamQueue = NoneQueue()
) -> bool:
    """
    使用缓存回答
    :return:
    """
    # (1) 先判断缓存是否存在
    min_score = 0.92
    answer_list = global_instance_milvus.search(
        collection_name=global_config["milvus"]["collection"]["aisearch_answer"],
        query=query,
        output_fields=["question", "answer"],
        limit=3
    )
    if len(answer_list) <= 0 or answer_list[0]["distance"] < min_score:
        return False
    question = answer_list[0]["entity"]["question"]
    answer = answer_list[0]["entity"]["answer"]
    answer_from_cache = f"## 问题\n{question}\n\n## 回答\n{answer}\n\n"

    # (2) 开始意图分析
    analyzer_result = Analyzer().analysis_intention_plan(
        query=query,
        messages=messages,
        queue=queue
    )

    # (3) 发送意图分析结果
    queue.send_message(
        type_str=STREAM_MESSAGE_ANALYZER_RESULT,
        item={
            "result": analyzer_result,
            "content": f"正在推理与规划中，已为你生成最佳规划，具体规划如下：{analyzer_result['thought']}"
        }
    )

    # (4) 准备输出过程
    queue.send_message(type_str=STREAM_MESSAGE_GENERATION_PENDING, item={"content": ""})
    global_instance_logger.log_info("aisearch answer_from_cache", {"answer_from_cache": answer_from_cache})

    # (5) 调用多样性丰富答案
    model_config = global_config["model"]["provider"]["deepseek_chat"]
    model = Model(model_type=model_config["model_type"], model_config=model_config)
    enrich_answer_generator = model.stream(
        langchain_input=[
            # System消息
            SystemMessage(system_prompt_template.format(answer_from_cache=answer_from_cache)),
            # 加入当前用户提问
            HumanMessage(user_prompt_template.format(query=query))
        ],
        config={
            "callbacks": make_chain_callbacks(
                langfuse_config=global_config["langfuse"],
                log_id=global_instance_localcache.get_log_id()
            )
        },
    )

    # (6) 拼接和输出答案
    enrich_answer = ""
    for item in enrich_answer_generator:
        enrich_answer += item.content
        queue.send_message(type_str=STREAM_MESSAGE_GENERATION, item={"content": item.content})

    # (7) 保存消息
    message_id = add_message(
        conversation_id=conversation_id,
        query=query,
        answer=enrich_answer
    )

    # (8) 流式接口结束
    end_data = {
        "code": COMMON_HTTP_CODE_SUCCESS,
        "conversation_id": conversation_id,
        "message_id": message_id,
        "mode": mode,
    }
    queue.send_message_end(data=end_data)
    return True
