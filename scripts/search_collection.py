"""
@File: search_collection.py
@Date: 2024/6/13 10:20
@desc: 搜索集合
"""
from wpylib.pkg.singleton.milvus.milvus import Milvus
import sys

# 创建客户端链接
client = Milvus(
    milvus_config={
        "uri": "http://127.0.0.1:19530",
        "host": "127.0.0.1",
        "port": "19530",
        "db_name": "milvus_aisearch",
        "collection": {
            "aisearch_answer": "aisearch_answer",
            "aisearch_movie": "aisearch_movie",
            "test": "test"
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


args = sys.argv[1:]
if len(args) != 2:
    print("请输入集合的名称和搜索的内容")
    exit(1)

collection_name = args[0]
if collection_name == "aisearch_answer":
    output_fields = ["id", "question", "answer"]
elif collection_name == "aisearch_movie":
    output_fields = ["id", "name"]
else:
    print(f"输入的Collection名称({collection_name})不存在")
    exit(1)

query = args[1].strip()
if query == "":
    print("请输入搜索的内容")
    exit(1)

# 本地启动milvus后, 可以访问http://127.0.0.1:9091/webui/在线查看
# 开始搜索
search_res = client.search(
    collection_name=collection_name,
    query=query,
    output_fields=output_fields
)
print(search_res)

# 查询所有数据
query_res = client.query(
    collection_name=collection_name,
    filter_str="id > 0",
    output_fields=output_fields
)
print(query_res)
