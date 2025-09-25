"""
@File: aisearch_by_openai_tool_calling.py
@Date: 2024/12/10 10:00
@Desc: 基于OpenAI的tool-calling实现AI搜索
"""
import os
import sys
import json
from openai import OpenAI
from web_search import search_web_tool, OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, WEBSEARCH_TOOL_DEFINITION

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 先调用模型并传递工具, 获取工具调用信息
messages = [
    {"role": "system", "content": "你是一个智能助手，"},
    {"role": "user", "content": "搜索北京今天的天气"},
]
model = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
llm_result = model.chat.completions.create(
    model=OPENAI_MODEL,
    messages=messages,
    stream=False,
    tools=[WEBSEARCH_TOOL_DEFINITION]
)
if hasattr(llm_result, "choices") and len(llm_result.choices) > 0 \
        and hasattr(llm_result.choices[0], "message") \
        and hasattr(llm_result.choices[0].message, "tool_calls") \
        and type(llm_result.choices[0].message.tool_calls) == list \
        and len(llm_result.choices[0].message.tool_calls) > 0:
    tool_call = llm_result.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)
    function_result_str = ""
    if function_name == "search_web_tool":
        function_result_str = search_web_tool(**function_args)  # 约定所有Tool都返回字符串
    # 拼接调用结果
    messages.extend([
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "function": {
                        "arguments": tool_call.function.arguments,
                        "name": function_name
                    },
                    "id": tool_call.id,
                    "type": "function"
                }
            ]
        },
        {"role": "tool", "tool_call_id": tool_call.id, "name": function_name, "content": function_result_str}
    ])
print(messages)

# 将工具调用结果传入上下文, 获取大模型的最终输出
llm_text_generator = model.chat.completions.create(
    model=OPENAI_MODEL,
    messages=messages,
    stream=True,
)
for chunk in llm_text_generator:
    # Get the current chunk content
    if not hasattr(chunk, 'choices') or not chunk.choices or not chunk.choices[0].delta.content:
        continue
    chunk_text = chunk.choices[0].delta.content
    print(chunk_text, end="", flush=True)
