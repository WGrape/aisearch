"""
@File: generator.py
@Date: 2024/12/10 10:00
@Desc: 生成器模块
"""
from wpylib.pkg.langchain.model import Model
from src.core.entity.search_result.outcome import Outcome
from src.core.entity.strategy.strategy import STRATEGY_MAP
from src.core.entity.search_result.result_set import ResultSet
from wpylib.pkg.langchain.chain import make_chain_callbacks
from src.core.entity.param.generator_param import GeneratorParam
from wpylib.pkg.sse.stream_queue import StreamQueue, NoneQueue
from langchain_core.prompts.chat import SystemMessage, HumanMessage
from src.init.init import global_config, global_instance_localcache
from src.core.entity.search_result.markdown_outcome import MarkdownOutcome
import re

STREAM_MESSAGE_GENERATION = "generation"
STREAM_MESSAGE_GENERATION_PENDING = "generation_pending"
STREAM_MESSAGE_REFERENCE = "reference"


class Generator:
    """
    生成器
    """
    _system_prompt_template: str = """
# 角色
{role}
## 注意
- 请输出标题
- 你将获得一组与问题相关的上下文，每个上下文都以参考编号开头，如 [citation:x]，其中x是一个数字。
- 如果回答中的某个句子引用了多个上下文，请在此句子末尾列出所有适用的引用，例如 [citation:3][citation:5]。
- 除了代码和特定名称和引用之外，你的答案必须使用与问题相同的语言编写。
## 上下文
{context}
## 回答策略
### 情感
{emotion}
### 风格
{answer_style}
## 目标
根据上下文中的参考信息，按照用户的要求执行。请以Markdown格式输出。
        """

    @staticmethod
    def _access_strategy_map(field_str) -> str:
        """
        通过解析传入的field_str字段名称，从STRATEGY_MAP常量中获取对应的strategy_value值，从而实现灵活选择不同的角色、情感、回答风格的效果。
        :param field_str:
        :return:
        """
        parts = field_str.split(".")

        strategy_value = STRATEGY_MAP
        for part in parts:
            strategy_value = strategy_value.get(part)
        return strategy_value

    def _select_role(self, generator_param: GeneratorParam):
        """
        选择角色
        :param generator_param:
        :return:
        """
        role = generator_param.get_strategy().get_role()
        return self._access_strategy_map(role)

    def _select_emotion(self, generator_param: GeneratorParam):
        """
        选择情感
        :param generator_param:
        :return:
        """
        emotion = generator_param.get_strategy().get_emotion()
        return self._access_strategy_map(emotion)

    def _select_answer_style(self, generator_param: GeneratorParam):
        """
        选择情感
        :param generator_param:
        :return:
        """
        answer_style = generator_param.get_strategy().get_answer_style()
        return self._access_strategy_map(answer_style)

    def generate(
            self,
            generator_param: GeneratorParam,
            result_set: ResultSet,
            messages: list = None,
            queue: StreamQueue = NoneQueue(),
    ) -> Outcome:
        """
        生成并输出
        """
        # 开始准备生成
        queue.send_message(type_str=STREAM_MESSAGE_GENERATION_PENDING, item={"content": ""})

        # 初始化model
        model_config = global_config["model"]["provider"]["deepseek_chat"]
        model = Model(model_type=model_config["model_type"], model_config=model_config)

        # 拼装并调用大模型
        system_prompt = self._system_prompt_template.format(
            role=self._select_role(generator_param=generator_param),
            context="\n\n".join(
                # 拼接联网搜索结果
                [
                    f"[citation:{c.get_doc_index()}] {c.select_as_citation()}" for i, c in
                    enumerate(result_set.get_web_document_list())
                ]
            ).join(
                # 拼接知识库结果
                [
                    f"[citation:{i+1}] {c.get_value()}" for i, c in
                    enumerate(result_set.get_knowledge_document_list())
                ]
            ),
            emotion=self._select_emotion(generator_param=generator_param),
            answer_style=self._select_answer_style(generator_param=generator_param),
        )
        user_prompt = generator_param.get_user_prompt()
        llm_text_generator = model.stream(
            langchain_input=[
                # System消息
                SystemMessage(system_prompt),
                # 加入当前用户提问
                HumanMessage(user_prompt)
            ],
            config={
                "callbacks": make_chain_callbacks(
                    langfuse_config=global_config["langfuse"],
                    log_id=global_instance_localcache.get_log_id()
                )
            },
        )

        # 输出内容
        llm_text = ""
        inside_think = False
        for item in llm_text_generator:
            llm_text += item.content
            # 如果使用DeepSeek模型, 需要舍去<think></think>标签内的思考部分, 此部分不作为答案。
            if not inside_think and "<think>" in llm_text:
                inside_think = True
                continue
            if inside_think:
                if "</think>" in llm_text:
                    # 思考过程结束, 但是</think>标签后可能有文本答案, 所以截取出来
                    inside_think = False
                    llm_text = llm_text.strip()
                    llm_text = re.sub(r'<think>.*?</think>', '', llm_text, flags=re.DOTALL)
                    if llm_text != "":
                        queue.send_message(type_str=STREAM_MESSAGE_GENERATION, item={"content": llm_text})
                continue
            # 输出答案
            queue.send_message(type_str=STREAM_MESSAGE_GENERATION, item={"content": item.content})

        # 当内容输出完成后，追加输出"\n\n"这两个换行符，以美化整体输出效果。
        if llm_text != "":
            footer = "\n\n"
            queue.send_message(type_str=STREAM_MESSAGE_GENERATION, item={"content": footer})
            llm_text += footer

        # 返回结果
        outcome = MarkdownOutcome(content=llm_text)
        return outcome
