from openai import OpenAI

client = OpenAI(api_key="")
response = client.files.create(
    file=open("mydata.jsonl", "rb"),
    purpose="fine-tune"
)
print(response)  # 其id字段表示上传成功后OpenAI返回的文件的ID，如"file-abc123"
