"""
@File: milvus_search_retriever.py
@Date: 2024/12/10 10:00
@Desc: 向量数据库的检索器模块
"""
from src.core.entity.search_result.result_set import ResultSet
from src.core.entity.param.retriever_param import RetrieverParam
from src.core.retriever.retriever import Retriever
from src.init.init import global_config, global_instance_logger, global_instance_milvus
from src.core.entity.search_result.result_set_item.knowledge_document import KnowledgeDocument


class MilvusSearchRetriever(Retriever):
    """
    milvus向量存储检索器
    """

    def retrieve(self, retriever_param: RetrieverParam) -> ResultSet:
        """
        执行入口
        :return:
        """
        # 解析参数
        query = retriever_param.get_query()
        count = retriever_param.get_count()
        min_score = retriever_param.get_min_score()

        # 开始搜索
        result_set = ResultSet()
        try:
            search_list = global_instance_milvus.search(
                collection_name=global_config["milvus"]["collection"]["aisearch_movie"],
                query=query,
                output_fields=["name", "description"],
                limit=count
            )
        except Exception as e:
            global_instance_logger.log_info(
                "aisearch milvus_search_retriever exception", {"e": e}
            )
            return result_set

        # 封装数据集
        if len(search_list) <= 0 or search_list[0]["distance"] < min_score:
            return result_set

        result_set = ResultSet()
        knowledge_document_list: list[KnowledgeDocument] = []
        for index, item in enumerate(search_list):
            document = KnowledgeDocument(
                key=search_list[index]["entity"]["name"],
                value=search_list[index]["entity"]["description"],
                score=search_list[index]["distance"]
            )
            knowledge_document_list.append(document)
        result_set.reset(knowledge_document_list=knowledge_document_list)

        # 返回数据集
        return result_set
