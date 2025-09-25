"""
@File: web_search.py
@Date: 2024/12/10 10:00
@Desc: 联网搜索工具
"""
from typing import Any
from langchain.tools import BaseTool
from langchain_community.utilities import BingSearchAPIWrapper, SearchApiAPIWrapper

SEARCHAPI_API_KEY = ""
OPENAI_API_KEY = ""
OPENAI_BASE_URL = "https://api.deepseek.com"
OPENAI_MODEL = "deepseek-chat"
OPENAI_MODEL_TYPE = "model_type_deepseek_chat"
MODEL_CONFIG = {
    "api_base": OPENAI_BASE_URL,
    "api_key": OPENAI_API_KEY,
    "model": OPENAI_MODEL,
    "model_type": OPENAI_MODEL_TYPE,
    "max_tokens": 512,
    "retry": 3,
}


class WebSearch:
    """
    必应搜索类
    """
    _engine: Any

    ENGINE_TYPE_BING = "bing"
    ENGINE_TYPE_GOOGLE = "google"
    ENGINE_TYPE_SEARCHAPI = "searchapi"

    def __init__(self, engine: str, engine_config: dict):
        if engine == self.ENGINE_TYPE_BING:
            self._engine = BingSearchAPIWrapper(
                bing_subscription_key=engine_config["bing_subscription_key"],
                bing_search_url=engine_config["bing_search_url"],
            )
        elif engine == self.ENGINE_TYPE_SEARCHAPI:
            self._engine = SearchApiAPIWrapper(
                engine="bing",
                searchapi_api_key=engine_config["searchapi_api_key"],
            )

    def search(self, query: str, count: int = 5) -> list:
        """
        开始搜索
        :return:
        """
        result: list = []
        if isinstance(self._engine, BingSearchAPIWrapper):
            search_list = self._engine.results(query=query, num_results=count)
            for search_item in search_list:
                result.append({
                    "title": search_item["title"],
                    "url": search_item["link"],
                    "icon": search_item["icon"],
                    "desc": search_item["snippet"],
                })
        elif isinstance(self._engine, SearchApiAPIWrapper):
            search_result = self._engine.results(query=query, num_results=count)
            for search_item in search_result["organic_results"]:
                result.append({
                    "title": search_item["title"],
                    "url": search_item["link"],
                    "icon": search_item["favicon"],
                    "desc": search_item["snippet"],
                })
        return result


def search_web_tool(query: str, count: int = 5) -> str:
    """
    联网搜索工具
    :param query: 搜索内容
    :param count: 搜索结果数量
    """
    result = WebSearch(engine=WebSearch.ENGINE_TYPE_SEARCHAPI, engine_config={
        "searchapi_api_key": SEARCHAPI_API_KEY,
    }).search(query=query, count=count)

    search_result_str = ""
    for k, item in enumerate(result):
        search_result_str += f"""[{k + 1}] 标题: {item["title"]} 链接: {item["url"]} 描述: {item["desc"]}\n"""
    search_context = f"=> 搜索行为 | 搜索内容：{query} | 搜索结果如下所示\n{search_result_str}"
    print(search_context)
    return search_context


class SearchWebTool(BaseTool):
    name = "search_web_tool"  # 名字必须符合正则^[a-zA-Z0-9_-]+$
    description = "联网搜索工具，通过网络搜索获取更详细更权威更实时的信息"

    def _run(self, query: str) -> str:
        return search_web_tool(query)

    def _arun(self, query: str) -> str:
        raise NotImplementedError("This tool does not support async")


WEBSEARCH_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "search_web_tool",
        "description": "联网搜索工具，通过网络搜索获取更详细更权威更实时的信息",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "需要进行网络搜索的搜索词",
                }
            },
            "required": ["query"],
            "additionalProperties": False
        },
    }
}

# result = WebSearch(engine=WebSearch.ENGINE_TYPE_SEARCHAPI, engine_config={
#     "searchapi_api_key": "",
# }).search("hello world", 5)
#
# print(result)
