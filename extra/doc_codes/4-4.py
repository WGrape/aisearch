import pandas as pd
from datasets import load_dataset

ds = load_dataset("lamini/lamini_docs")  # 加载名为lamini/lamini_docs"的数据集
train_dataset = ds['train']  # 只使用训练集
train_df = pd.DataFrame(train_dataset)
questions_answers = train_df[['question', 'answer']]
for index, example in questions_answers.iterrows():
    print(f"question: {example['question']}\n answer: {example['answer']}\n\n")
