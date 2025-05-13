"""
@File: test.py
@Date: 2024/12/10 10:00
@desc: 测试文件
"""
from scrapyer.items import ScrapyerItem

if __name__ == '__main__':
    item = ScrapyerItem(movie_id=1, name="喜剧之王")
    print(item.keys())
    print(item["movie_id"])
    print(item["name"])