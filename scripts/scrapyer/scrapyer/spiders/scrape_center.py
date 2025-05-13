"""
@File: scrape_center.py
@Date: 2024/6/13 10:20
@desc: 爬虫文件
"""
from typing import Any
from scrapy.http import Response
from scrapyer.items import ScrapyerItem  # 忽视IDE的报错, 会自动加载此模块
import scrapy
import json


class ScrapeCenterSpider(scrapy.Spider):
    """
    爬虫类
    """
    name = "scrape_center"
    allowed_domains = ["scrape.center"]
    start_urls = ["https://scrape.center/"]

    def __init__(self, **kwargs: Any):
        """
        初始化数据库连接
        :param kwargs:
        """
        super().__init__(**kwargs)

    def open_spider(self, spider):
        """
        开启爬虫时执行，只执行一次
        :param spider: 爬虫对象
        :return:
        """
        print("open_spider ...")

    def start_requests(self):
        """
        开始请求
        """
        # 生成 ID 1 到 10 的页面
        for movie_id in range(1, 11):
            url = f"https://ssr1.scrape.center/detail/{movie_id}"
            yield scrapy.Request(url, callback=self.parse, meta={"movie_id": movie_id})

    def parse(self, response: Response, **kwargs: Any):
        """
        解析页面
        :param response: 响应对象
        :param kwargs:
        :return:
        """
        movie_id = response.meta["movie_id"]  # 获取传递的ID

        context = response.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/a/h2/text()')
        name = context.extract_first() or ""

        categories = response.xpath('//button[contains(@class, "category")]/span/text()').getall()
        category = json.dumps(categories, ensure_ascii=False) or ""

        context = response.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[2]/span[3]/text()')
        duration = context.extract_first() or ""

        context = response.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[2]/span[1]/text()')
        country = context.extract_first() or ""

        context = response.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[3]/span/text()')
        showtime = context.extract_first() or ""

        context = response.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[4]/p/text()')
        description = context.extract_first() or ""

        context = response.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[3]/p[1]/text()')
        score = context.extract_first() or ""

        item = ScrapyerItem(
            movie_id=movie_id,
            name=name,
            category_json=category,
            duration=duration,
            country_json=country,
            showtime=showtime,
            description=description,
            score=score,
        )
        yield item

    def close_spider(self, spider):
        """
        关闭爬虫时执行，只执行一次
        :param spider: 爬虫对象
        :return:
        """
        print("close_spider ...")
