"""
@File: mindmap_outcome.py
@Date: 2024/12/10 10:00
@Desc: 结果内容部分的markdown格式
"""
from src.core.entity.search_result.outcome import Outcome, OUTCOME_TYPE_MINDMAP


class MindmapOutcome(Outcome):
    """
    mindmap格式的结果
    """

    def __init__(self, content: str):
        super().__init__(content=content, content_type=OUTCOME_TYPE_MINDMAP)
