from wpylib.pkg.singleton.milvus.milvus import Milvus

# 创建客户端链接
client = Milvus(
    milvus_config={
        "uri": "http://127.0.0.1:19530",
        "host": "127.0.0.1",
        "port": "19530",
        "db_name": "milvus_aisearch",
        "collection": {
            "aisearch_answer": "aisearch_answer",
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

# collection名称
collection_name = "test"

# 插入数据
question1 = "他生病了所以那天早上没有来"
question2 = "他生气了所以那天早上没有来"
embedding1 = client.embed(question1)
embedding2 = client.embed(question2)
data = [
    {
        "vector": embedding1,
        "name": question1,
    },
    {
        "vector": embedding2,
        "name": question2,
    },
]
res = client.insert(
    collection_name=collection_name,
    data=data
)
print(res)

# 查询question2
res = client.search(
    collection_name=collection_name,
    query=question2,
    output_fields=["id", "name"]
)
print(res)
