"""
@File: predict.py
@Date: 2024/1/29 19:41
@Desc: 生成预测问题的逻辑
"""
from wpylib.pkg.langchain.model import Model
from src.dao.message import get_message_list
from wpylib.util.x.xjson import extract_first_json
from wpylib.pkg.langchain.history import make_conversation_history
from src.init.init import global_config, global_instance_localcache
from wpylib.pkg.langchain.prompt import create_chat_prompt_by_messages
from wpylib.pkg.langchain.chain import create_chain, make_chain_callbacks
from langchain_core.prompts.chat import SystemMessage, HumanMessagePromptTemplate


def gen_predict_questions(conversation_id: int):
    """
    生成预测问题
    :param conversation_id: 会话ID
    :return:
    """
    system_prompt = """
    # 角色
    你是一个AI智能预测助手，你可以精准的预测用户下次的提问。
    ## 要求
    1. 预测的问题长度不要超过25个字
    2. 返回结构如下：
    ```json
    {
        "questions": [
            ""
        ]
    }
    ```
    ## 工作流
    1. 先认真读取用户给你的<ConversationHistory></ConversationHistory>会话历史。
    2. 预测用户下一次可能会提问的问题。
    3. 按照要求返回。
    ## 目标
    通过分析用户给你的对话历史，分析用户下一次可能会提问的问题。
        """

    # 创建大模型
    model_config = global_config["model"]["provider"]["deepseek_chat"]
    model = Model(model_type=model_config["model_type"], model_config=model_config)
    prompt = create_chat_prompt_by_messages(messages=[
        SystemMessage(content=system_prompt),
        HumanMessagePromptTemplate.from_template("{input}"),
    ])
    chain = create_chain(
        model=model.get_raw_model(),
        prompt=prompt,
    )

    # 调用大模型生成总结结果
    questions = []
    messages = get_message_list(where={"conversation_id": conversation_id, "deleted": 0})
    user_prompt = make_conversation_history(messages=messages, only_user=True)
    llm_invoke = chain.invoke(
        input=user_prompt,
        config={
            "callbacks": make_chain_callbacks(
                langfuse_config=global_config["langfuse"],
                log_id=global_instance_localcache.get_log_id()
            )
        }
    )
    llm_result = extract_first_json(llm_invoke["text"])
    if "questions" in llm_result:
        questions = llm_result["questions"]

    # 返回预测的问题
    return questions
