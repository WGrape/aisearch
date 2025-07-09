import pandas as pd
from datasets import load_dataset

ds = load_dataset("lamini/lamini_docs")  # 加载名为lamini/lamini_docs"的数据集
train_dataset = ds['train']  # 只使用训练集
train_df = pd.DataFrame(train_dataset)
questions_answers = train_df[['question', 'answer']]
for index, example in questions_answers.iterrows():
    print(f"question: {example['question']}\n answer: {example['answer']}\n\n")

# ===============================================================================
import json

with open('finetune_train_data.jsonl', 'w') as jsonl_file:
    for index, example in questions_answers.iterrows():
        formatted_data = {
            "messages": [
                {"role": "system", "content": "You're a helpful assistant"},
                {"role": "user", "content": example['question']},
                {"role": "assistant", "content": example['answer']}
            ]
        }
        jsonl_file.write(json.dumps(formatted_data) + "\n")  # '\\n' 修复为 "\n"
