from openai import OpenAI
import pandas as pd

client = OpenAI(
    api_key="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",  # 替换为你的API密钥
)


def get_embedding(text, model="text-embedding-3-small"):
    """ 使用 OpenAI API 获取文本的嵌入向量 """
    text = text.replace("\n", " ")  # 替换换行符，以保持文本的连贯性
    return client.embeddings.create(input=[text], model=model).data[0].embedding



df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-3-small'))
df.to_csv('output/embedded_1k_reviews.csv', index=False)

# 文件路径
file_path = '三国演义.txt'

# 读取文件
with open(file_path, 'r', encoding='utf-16') as file:
    text = file.read()

# 为了示例，假设我们只处理前1000个字符
sample_text = text[:1000]

# 将文本分割为句子或段落
sentences = sample_text.split('\n')  # 假设每个段落由换行符分隔

# 使用 OpenAI 的 embedding 模型向量化文本
embeddings = openai.Embedding.create(
    model="text-embedding-3-small",
    input=sentences
)

# 打印向量结果
for emb in embeddings['data']:
    print(emb['embedding'])
