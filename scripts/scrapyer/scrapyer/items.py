"""
@File: items.py
@Date: 2024/6/13 10:20
@desc: 目标文件
"""
import scrapy


class ScrapyerItem(scrapy.Item):
    """
    爬取目标实体类
    """
    movie_id = scrapy.Field()  # 电影的ID字段
    name = scrapy.Field()  # 电影的名称字段
    category_json = scrapy.Field()  # 电影的分类字段
    duration = scrapy.Field()  # 电影的时长字段
    country_json = scrapy.Field()  # 电影的国家字段
    showtime = scrapy.Field()  # 电影的上映时间字段
    description = scrapy.Field()  # 电影的描述字段
    score = scrapy.Field()  # 电影的评分字段
    pass
