"""
@File: bing_search_retriever.py
@Date: 2024/12/10 10:00
@Desc: 必应搜索检索器模块
"""
from wpylib.util.encry import sha1
from src.init.init import global_config
from src.core.entity.search_result.result_set import ResultSet
from src.core.entity.param.retriever_param import RetrieverParam
from langchain_community.utilities import BingSearchAPIWrapper
from src.core.retriever.retriever import Retriever
from src.core.entity.search_result.result_set_item.web_document import WebDocument
import urllib.parse


class BingSearchRetriever(Retriever):
    """
    必应搜索检索器
    """
    _WEB_DOCUMENT_RESOURCE_MAP = {
        "baike.baidu.com": {
            "name": "百度百科",
            "icon": "https://baike.baidu.com/favicon.ico",
        },
    }
    _instance_bing_search = BingSearchAPIWrapper(
        bing_subscription_key=global_config["bing"]["bing_subscription_key"],
        bing_search_url=global_config["bing"]["bing_search_url"],
    )

    def retrieve(self, retriever_param: RetrieverParam) -> ResultSet:
        """
        执行入口
        :return:
        """
        # 解析参数
        query = retriever_param.get_query()
        count = retriever_param.get_count()
        start_index = retriever_param.get_start_index()

        # 开始搜索
        search_list = self._instance_bing_search.results(query, count)
        # 搜索接口可能返回无结果: search_list = [{'Result': 'No good Bing Search Result was found'}]

        # 封装数据集
        result_set = ResultSet()
        web_document_list: list[WebDocument] = []
        for k, item in enumerate(search_list):
            if "snippet" not in item or item["snippet"] == "":
                continue
            # 参数检查, 有时候必应接口返回的字段会缺少link
            if "link" not in item:
                item["link"] = ""
            # 文档资源信息
            source = ""
            resource_info = {
                "name": "网页",
                "icon": "",
            }
            if item["link"].startswith("http:/") or item["link"].startswith("https:/"):
                source = urllib.parse.urlparse(item["link"]).netloc
                if source in self._WEB_DOCUMENT_RESOURCE_MAP:
                    resource_info = self._WEB_DOCUMENT_RESOURCE_MAP[source]
            # 文档结构体
            web_document = WebDocument(
                doc_index=start_index + k + 1,
                doc_id=f"""{sha1(item["link"])}""",
                title=item.get("title", ""),
                description=item.get("snippet", "")[:1000],
                icon=resource_info["icon"],
                url=item["link"],
                source=source,
                source_name=resource_info["name"],
                content="",
            )

            # 加入到web_document列表中
            web_document_list.append(web_document)
        result_set.reset(web_document_list=web_document_list)

        # 返回数据集
        return result_set
