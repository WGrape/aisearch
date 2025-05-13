"""
@File: output_action.py
@Date: 2024/12/10 10:00
@Desc: 输出动作类
"""
from src.core.entity.search_result.outcome import Outcome
from src.core.entity.search_result.result_set import ResultSet
from src.core.entity.param.generator_param import GeneratorParam
from wpylib.pkg.sse.stream_queue import StreamQueue, NoneQueue
from src.core.generator.generator import Generator
from src.work.scheduler.action.action import Action


class OutputAction(Action):
    """
    输出动作
    """
    _name = "output"
    _generator: Generator

    def __init__(self):
        super().__init__()
        self._generator = Generator()

    def do(
            self,
            generator_param: GeneratorParam,
            result_set: ResultSet,
            messages: list = None,
            queue: StreamQueue = NoneQueue(),
    ) -> Outcome:
        """
        开始执行
        """
        # (1) 开始生成
        outcome = self._generator.generate(
            generator_param=generator_param,
            result_set=result_set,
            messages=messages,
            queue=queue,
        )

        # (2) 返回结果
        outcome = Outcome(content=outcome.get_content())
        return outcome
