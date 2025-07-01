from openai import OpenAI

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "你是一个智能助手，名字叫聪聪"},
        {"role": "user", "content": "你好，你是谁？"},
    ],
    stream=True
)

for chunk in response:
    if chunk.choices:
        # DeepSeek流式返回的数据结构中，每个chunk里的choices[0]是一个对象，它的delta.content存储着新生成的文本
        delta = chunk.choices[0].delta
        if hasattr(delta, "content") and delta.content:
            print(delta.content, end="", flush=True)  # 逐步输出推理过程
