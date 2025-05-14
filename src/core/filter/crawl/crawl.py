"""
@File: crawl.py
@Date: 2024/12/10 10:00
"""
import asyncio
from wpylib.util.encry import sha1
from src.init.init import global_instance_logger
from src.init.init import global_instance_localcache
from src.core.filter.filter import Filter
from src.core.entity.search_result.result_set import ResultSet
from src.dao.crawl import add_crawl_record_list, get_crawl_record
from src.core.entity.search_result.result_set_item.web_document import WebDocument
from wpylib.pkg.singleton.loader.web_loader import WebLoader, WEB_LOADER_ENGINE_JINA


class Crawl(Filter):
    """
    读取器
    """

    # 定义使用JINA引擎的网页加载器
    _web_loader: WebLoader = WebLoader(engine=WEB_LOADER_ENGINE_JINA)

    def _crawl_web_document(self, log_id, item: WebDocument) -> WebDocument:
        """
        读取网页内容
        :param item: Web文档
        :return:
        """
        # 1. 先尝试从本地中获取网页内容
        new_web_document: WebDocument = item
        global_instance_localcache.set_log_id(log_id)
        is_crawled, crawl_record = get_crawl_record(new_web_document.get_doc_id())

        # 2. 如果该网页已被读取且被拉黑
        if is_crawled and int(crawl_record["deleted"]) == 1:
            global_instance_logger.log_info(
                "aisearch crawl been delete", {"crawl_record_id": crawl_record["id"]}
            )
            return new_web_document

        # 3. 如果该网页在本地存在, 则直接读取本地网页
        if is_crawled and crawl_record["content"] != "":
            # 更新文档信息
            new_web_document.update_title(crawl_record["title"])
            new_web_document.update_description(crawl_record["description"])
            new_web_document.update_content(crawl_record["content"])
            new_web_document.update_hit_count(crawl_record["hit_count"])
            # 打印日志
            global_instance_logger.log_info(
                "aisearch crawl hit and not need re-crawl", biz_data={"doc_id": new_web_document.get_doc_id()}
            )
            return new_web_document

        # 4. 重新读取网页
        crawl_docs = []
        try:
            crawl_docs = self._web_loader.load(
                resource_info_list=[
                    {
                        "url": new_web_document.get_url(),
                        "source": new_web_document.get_source()
                    }
                ],
                headers={"X-Timeout": "60"}
            )
            global_instance_logger.log_info("aisearch crawl first", biz_data={
                "crawl_docs": crawl_docs,
                "url": new_web_document.get_url(),
                "doc_id": sha1(new_web_document.get_url())
            })
        except Exception as e:
            # 解析网页失败, 直接跳过
            global_instance_logger.log_error("aisearch crawl error", {"e": e, "url": new_web_document.get_url()})
        if len(crawl_docs) <= 0:
            return new_web_document

        # 5. 更新文档信息
        new_web_document.update_title(crawl_docs[0].get_title() or "无法获取")
        new_web_document.update_description(crawl_docs[0].get_description() or "无法获取")
        new_web_document.update_content(crawl_docs[0].get_content() or "无法获取")
        return new_web_document

    def choose(self, result_set: ResultSet, **kwargs) -> ResultSet:
        """
        统一读取入口
        :return:
        """
        # 在当前线程内创建事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        log_id = global_instance_localcache.get_log_id()
        tasks = [
            asyncio.wait_for(loop.run_in_executor(None, self._crawl_web_document, log_id, item), timeout=600)
            for item in result_set.get_web_document_list()
        ]
        try:
            new_web_document_list = loop.run_until_complete(asyncio.gather(*tasks))
        except asyncio.TimeoutError:
            global_instance_logger.log_error("aisearch crawl timeout error")
            new_web_document_list = result_set.get_web_document_list()
        finally:
            loop.close()

        # 保存网页内容记录
        crawl_id_list = add_crawl_record_list(new_web_document_list)

        # 返回结果集
        result_set.reset(
            web_document_list=new_web_document_list, crawl_id_list=crawl_id_list
        )
        return result_set
