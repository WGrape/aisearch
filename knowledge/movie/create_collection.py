"""
@File: create_collection.py
@Date: 2024/6/13 10:20
@desc: 创建集合
"""
from pymilvus import MilvusClient, DataType
from wpylib.pkg.singleton.milvus.milvus import Milvus

# 创建客户端链接
client = Milvus(
    milvus_config={
        "uri": "http://127.0.0.1:19530",
        "host": "127.0.0.1",
        "port": "19530",
        "db_name": "milvus_aisearch",
        "collection": {
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
client = client.get_instance_milvus()

# 如果存在此Collection则删除
collection_name = "aisearch_movie"
if client.has_collection(collection_name=collection_name):
    client.drop_collection(collection_name=collection_name)

# 定义schema
schema = MilvusClient.create_schema(
    auto_id=True,
    enable_dynamic_field=True,
)

# 设置schema字段
schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
schema.add_field(field_name="movie_id", datatype=DataType.INT64)
schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768)
schema.add_field(field_name="name", datatype=DataType.VARCHAR, max_length=512)
schema.add_field(field_name="description", datatype=DataType.VARCHAR, max_length=4096)

# 创建索引
index_params = MilvusClient.prepare_index_params()
index_params.add_index(
    field_name="vector",
    metric_type="COSINE",
    index_type="IVF_FLAT",
    index_name="vector_index",
    params={"nlist": 128}
)

# 基于schema创建
client.create_collection(
    collection_name=collection_name,
    schema=schema,
    index_params=index_params
)

# 打印Collection列表
print(client.list_collections())
