from openai import OpenAI

client = OpenAI(api_key="")
response = client.files.create(
    file=open("mydata.jsonl", "rb"),
    purpose="fine-tune"
)
print(response)  # 其id字段表示上传成功后OpenAI返回的文件的ID，如"file-abc123"

# ========================================

from openai import OpenAI

client = OpenAI(api_key="")
response = client.fine_tuning.jobs.create(
    training_file=response.id,  # 使用上一步文件上传成功后返回的文件ID，如"file-abc123"
    model="gpt-4o-mini"
)
print(response)  # 其id字段表示创建微调任务成功后OpenAI返回的任务ID，如“ftjob-abc123”
