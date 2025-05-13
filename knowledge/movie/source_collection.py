"""
@File: source_collection.py
@Date: 2024/6/13 10:20
@desc: 数据同步aisearch_movie集合
"""
from wpylib.pkg.singleton.milvus.milvus import Milvus
import pymysql

# 创建客户端链接
client = Milvus(
    milvus_config={
        "uri": "http://127.0.0.1:19530",
        "host": "127.0.0.1",
        "port": "19530",
        "db_name": "milvus_aisearch",
        "collection": {
            "aisearch_movie": "aisearch_movie",
            "test": "test",
        }
    },
    model_config={
        "api_base": "http://localhost:11434",
        "api_key": "ollama",
        "embedding_dims": 768,
        "model": "nomic-embed-text",
        "model_type": "embedding_type_nomic",
        "retry": 3,
    }
)
# client = client.get_instance_milvus()

# collection名称
collection_name = "aisearch_movie"


# 开始同步
def sync_movie_from_mysql():
    """从 MySQL 读取所有电影数据"""
    # 连接数据库
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="temp_aisearch",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # 读取所有未删除的电影数据
            sql = "SELECT id, name, category_json, duration, country_json, showtime, description, score FROM aisearch_knowledge_movie WHERE deleted = 0;"
            cursor.execute(sql)
            movies: list[dict] = cursor.fetchall()

            for movie in movies:
                movie_id = movie["id"]
                name = movie["name"]
                category_json = movie["category_json"]
                duration = movie["duration"]
                country_json = movie["country_json"]
                showtime = movie["showtime"]
                description = movie["description"]
                score = movie["score"]

                # 处理数据
                print(f"电影ID: {movie_id}, 名称: {name}, 评分: {score}")

                # 插入向量数据库
                name_embedding = client.embed(name)
                data = [
                    {
                        "movie_id": movie_id,
                        "vector": name_embedding,
                        "name": name,
                        "category_json": category_json,
                        "duration": duration,
                        "country_json": country_json,
                        "showtime": showtime,
                        "description": description,
                        "score": score,
                    }
                ]
                res = client.insert(
                    collection_name=collection_name,
                    data=data
                )
                print(res)  # {'insert_count': 1, 'ids': [1]}
    except Exception as e:
        print(f"查询数据失败: {e}")
    finally:
        connection.close()


sync_movie_from_mysql()
