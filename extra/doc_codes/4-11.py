from openai import OpenAI

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个智能助手，名字叫聪聪"},
        {"role": "user", "content": "你好，你是谁？"},
    ],
    stream=False
)

print(response.choices[0].message.content)
