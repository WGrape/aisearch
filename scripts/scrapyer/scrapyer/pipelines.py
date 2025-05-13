"""
@File: pipelines.py
@Date: 2024/6/13 10:20
@desc: 管道文件
"""
from wpylib.util.x.xjson import stringify
from wpylib.pkg.singleton.mysql.mysql import Mysql


class ScrapyerPipeline:
    """
    管道类
    """

    def __init__(self):
        self.connection = Mysql(mysql_config={
            "dsn": {
                "host": "127.0.0.1",
                "database": "temp_aisearch",
                "user": "root",
                "password": "",
                "port": 3306,
                "connect_timeout": 10
            },
            "retry": 3,
        })

    def process_item(self, item, spider):
        """
        处理数据
        :param item: 目标数据
        :param spider: 爬虫对象
        :return:
        """
        item["movie_id"] = int(item["movie_id"])
        item["name"] = item["name"].strip()
        item["category_json"] = item["category_json"]
        item["duration"] = item["duration"].strip()
        item["country_json"] = item["country_json"].strip()
        item["showtime"] = item["showtime"].strip()
        item["description"] = item["description"].strip()
        item["score"] = float(item["score"]) or 0.0

        # 存储数据并返回
        self.save_to_mysql(data=item)
        self.save_to_file(data=item)
        return item

    def save_to_file(self, data):
        """
        保存到文件
        :param data: 数据内容
        :return:
        """
        filename = f"scrape_center_movie.jsonl"
        with open(filename, 'a') as f:
            f.write(stringify({
                "movie_id": data["movie_id"],
                "name": data["name"],
                "category_json": data["category_json"],
                "duration": data["duration"],
                "country_json": data["country_json"],
                "showtime": data["showtime"],
                "description": data["description"],
                "score": data["score"],
            }) + "\n")

    def save_to_mysql(self, data):
        """
        保存数据到MySQL
        :param data: 数据内容
        :return:
        """
        insert_sql = """
               INSERT INTO aisearch_knowledge_movie (`id`, `name`, category_json, duration, country_json, showtime, `description`, `score`) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE 
                   `name` = VALUES(`name`),
                   category_json = VALUES(category_json),
                   duration = VALUES(duration),
                   country_json = VALUES(country_json),
                   showtime = VALUES(showtime),
                   `description` = VALUES(`description`),
                   `score` = VALUES(`score`);
           """
        self.connection.execute_raw_query(query=insert_sql, params=[
            data["movie_id"],
            data["name"],
            data["category_json"],
            data["duration"],
            data["country_json"],
            data["showtime"],
            data["description"],
            data["score"]
        ])
