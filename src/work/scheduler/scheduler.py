"""
@File: scheduler.py
@Date: 2024/12/10 10:00
@Desc: 调度器模块
"""
from src.core.entity.plan.plan import Plan
from src.core.entity.search_result.outcome import Outcome
from wpylib.pkg.sse.stream_queue import StreamQueue, NoneQueue
from src.core.entity.search_result.result_set import ResultSet
from src.core.entity.param.generator_param import GeneratorParam
from src.core.entity.param.retriever_param import RetrieverParam
from src.work.scheduler.action.output_action import OutputAction
from src.work.scheduler.action.search_web_action import SearchWebAction
from src.core.entity.schedule_result.schedule_result import ScheduleResult
from src.work.scheduler.action.search_local_action import SearchLocalAction
from src.work.scheduler.action.search_web_and_output_action import SearchWebAndOutputAction
from src.core.analyzer.analyzer import INTENTION_TYPE_NONE, ACTION_TYPE_END, ACTION_TYPE_OUTPUT, \
    ACTION_TYPE_SEARCH_WEB, ACTION_TYPE_SEARCH_LOCAL, ACTION_TYPE_SEARCH_WEB_AND_OUTPUT, \
    ACTION_TYPE_SEARCH_LOCAL_AND_OUTPUT
from src.work.scheduler.action.search_local_and_output_action import SearchLocalAndOutputAction


class Scheduler:
    """
    调度器
    """
    # 基本属性
    _search_web_action: SearchWebAction
    _search_local_action: SearchLocalAction
    _output_action: OutputAction
    _search_web_and_output_action: SearchWebAndOutputAction
    _search_local_and_output_action: SearchLocalAndOutputAction

    def __init__(self):
        self._search_web_action = SearchWebAction()
        self._output_action = OutputAction()
        self._search_web_and_output_action = SearchWebAndOutputAction()
        self._search_local_and_output_action = SearchLocalAndOutputAction()

    def _loop(
            self,
            plan: Plan,
            messages: list = None,
            queue: StreamQueue = NoneQueue(),
            **kwargs
    ) -> ScheduleResult:
        """
        自动调度方法
        :param plan:
        :param messages:
        :param queue:
        :return:
        """
        filter_list = []
        if "filter_list" in kwargs:
            filter_list = kwargs["filter_list"]

        # 循环动作列表
        start_index = 0
        result_set_list: list[ResultSet] = []
        outcome_list: list[Outcome] = []
        for action_item in plan.get_action_list():
            if "type" not in action_item:
                continue
            action_type = action_item["type"].lower()

            if action_type == ACTION_TYPE_END:
                continue
            elif action_type == ACTION_TYPE_SEARCH_WEB:
                result_set = self._search_web_action.do(
                    search_web_param=RetrieverParam(
                        query=plan.get_query() + " " + action_item["part"],
                        count=3,
                        start_index=start_index,
                    ),
                    filter_list=filter_list,
                    queue=queue
                )
                result_set_list.append(result_set)
                start_index += len(result_set.get_web_document_list())
            elif action_type == ACTION_TYPE_SEARCH_LOCAL:
                result_set = self._search_local_action.do(
                    search_local_param=RetrieverParam(
                        query=plan.get_query() + " " + action_item["part"],
                        count=3,
                        min_score=0.92,
                    ),
                    queue=queue
                )
                result_set_list.append(result_set)
            elif action_type == ACTION_TYPE_OUTPUT:
                outcome = self._output_action.do(
                    generator_param=GeneratorParam(
                        query=action_item["part"],
                        query_rewriting=plan.get_query_rewriting(),
                        query_domain=plan.get_query_domain(),
                        strategy=plan.get_strategy(),
                        user_prompt=plan.get_user_prompt().format(
                            title=action_item["part"],
                            previous_output="\n".join([obj.get_content() for obj in outcome_list])
                        )
                    ),
                    result_set=ResultSet.combine(result_set_list),  # 在处理仅输出动作时，由于前面可能已累计多个查询结果, 因此需要合并这些搜索结果，以便作为上下文使用。
                    messages=messages,
                    queue=queue
                )
                # outcome
                outcome_list.append(outcome)
            elif action_type == ACTION_TYPE_SEARCH_WEB_AND_OUTPUT:
                result_set, outcome = self._search_web_and_output_action.do(
                    search_web_param=RetrieverParam(
                        query=plan.get_query() + " " + action_item["part"],
                        count=3,
                        start_index=start_index,
                    ),
                    generator_param=GeneratorParam(
                        query=action_item["part"],
                        query_rewriting=plan.get_query_rewriting(),
                        query_domain=plan.get_query_domain(),
                        strategy=plan.get_strategy(),
                        user_prompt=plan.get_user_prompt().format(
                            title=action_item["part"],
                            previous_output="\n".join([obj.get_content() for obj in outcome_list])
                        )
                    ),
                    filter_list=filter_list,
                    messages=messages,
                    queue=queue
                )
                # outcome
                outcome_list.append(outcome)
                # result_set
                result_set_list.append(result_set)
                start_index += len(result_set.get_web_document_list())
            elif action_type == ACTION_TYPE_SEARCH_LOCAL_AND_OUTPUT:
                result_set, outcome = self._search_local_and_output_action.do(
                    search_local_param=RetrieverParam(
                        query=plan.get_query() + " " + action_item["part"],
                        count=3,
                        min_score=0.92,
                    ),
                    generator_param=GeneratorParam(
                        query=action_item["part"],
                        query_rewriting=plan.get_query_rewriting(),
                        query_domain=plan.get_query_domain(),
                        strategy=plan.get_strategy(),
                        user_prompt=plan.get_user_prompt().format(
                            title=action_item["part"],
                            previous_output="\n".join([obj.get_content() for obj in outcome_list])
                        )
                    ),
                    messages=messages,
                    queue=queue
                )
                # outcome
                outcome_list.append(outcome)
                # result_set
                result_set_list.append(result_set)

        # 返回调度结果
        return ScheduleResult(
            plan=plan,
            result_set=ResultSet.combine(result_set_list),
            outcome=Outcome.combine(outcome_list),
        )

    def _handle_common_intention(
            self,
            plan: Plan,
            messages: list = None,
            queue: StreamQueue = NoneQueue(),
            **kwargs
    ):
        """
        通用意图处理
        :param plan:
        :param messages:
        :param queue:
        :param kwargs:
        :return:
        """
        return self._loop(
            plan=plan,
            messages=messages,
            queue=queue,
            **kwargs
        )

    def _handle_none_intention(
            self,
            plan: Plan,
            messages: list = None,
            queue: StreamQueue = NoneQueue(),
            **kwargs
    ):
        """
        None意图处理
        :return:
        """
        result_set = ResultSet()
        outcome = self._output_action.do(
            generator_param=GeneratorParam(
                query=plan.get_query(),
                query_rewriting=plan.get_query_rewriting(),
                query_domain=plan.get_query_domain(),
                strategy=plan.get_strategy(),
                user_prompt=plan.get_user_prompt().format(
                    title=plan.get_query(),
                    previous_output="",
                ),
            ),
            result_set=result_set,
            messages=messages,
            queue=queue
        )

        # 返回调度结果
        return ScheduleResult(
            plan=plan,
            result_set=result_set,
            outcome=outcome,
        )

    def schedule(
            self,
            plan: Plan,
            messages: list = None,
            queue: StreamQueue = NoneQueue(),
            **kwargs
    ) -> ScheduleResult:
        """
        开始调度
        """
        # 开始
        intention = plan.get_intention()

        # 1. 如果是大模型意图
        if intention == INTENTION_TYPE_NONE:
            schedule_result = self._handle_none_intention(
                plan=plan,
                messages=messages,
                queue=queue,
                **kwargs
            )
            # 返回结果
            return schedule_result

        # 2. 根据不同意图选择不同处理方式
        schedule_result = self._handle_common_intention(
            plan=plan,
            messages=messages,
            queue=queue,
            **kwargs
        )

        # 返回结果
        return schedule_result
