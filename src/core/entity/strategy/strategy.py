"""
@File: strategy.py
@Date: 2024/12/10 10:00
"""

STRATEGY_MAP = {
    "role": {
        "simple": "你是一个简洁直观的AI助手",
        "professional": "你是一个专业领域内的专家",
    },
    "emotion": {
        "simple": "保持正面、积极、乐观的情绪和态度",
        "professional": "保持严谨、专业、客观的表达方式",
    },
    "answer_style": {
        "simple": "用简洁直接的方式回答问题，不做过多扩展，确保核心信息清晰易懂。",
        "professional": "回答需具备专业性，引用权威资料，并进行深入分析，逻辑清晰、结构完整，适用于专业人士阅读。",
    },
}
ROLE_SIMPLE: str = "role.simple"
EMOTION_SIMPLE: str = "emotion.simple"
ANSWER_STYLE_SIMPLE: str = "answer_style.simple"

ROLE_PROFESSIONAL: str = "role.professional"
EMOTION_PROFESSIONAL: str = "emotion.professional"
ANSWER_STYLE_PROFESSIONAL: str = "answer_style.professional"


class Strategy:
    """
    生成策略: generator在回答时应该使用的策略
    """
    _role: str = ROLE_SIMPLE
    _emotion: str = EMOTION_SIMPLE
    _answer_style: str = ANSWER_STYLE_SIMPLE

    def __init__(
            self,
            role: str = ROLE_SIMPLE,
            emotion: str = EMOTION_SIMPLE,
            answer_style: str = ANSWER_STYLE_SIMPLE,
    ):
        self._role = role
        self._emotion = emotion
        self._answer_style = answer_style

    def get_role(self) -> str:
        """
        获取角色_role
        :return:
        """
        return self._role

    def get_emotion(self) -> str:
        """
        获取情感_emotion
        :return:
        """
        return self._emotion

    def get_answer_style(self) -> str:
        """
        获取回答风格_answer_style
        :return:
        """
        return self._answer_style
