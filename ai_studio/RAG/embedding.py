import re
import numpy as np
from openai import OpenAI
import pandas as pd
from ai_studio.Chat2AI import chat_with_ai
from numpy.linalg import norm
import tiktoken

# 初始化 OpenAI 客户端
client = OpenAI()


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_embedding(text, model="text-embedding-3-small"):
    """ 使用 OpenAI API 获取文本的嵌入向量 """
    text = text.replace("\n", " ")  # 替换换行符，以保持文本的连贯性
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def load_text_file(file_path):
    """ 读取整个文本文件 """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


#用'%$#@!' 文本是被分割后的文本的前半段  用'!@#$%'代表文本是被分割后的文本的后半段   方便后续进行拼接
def split_text_to_fit_token_limit(text, max_tokens=8000, split_prefix='%$#@!', split_suffix='!@#$%'):
    """ 递归分割文本，确保每段的 token 数量不超过 max_tokens，并添加特定标识符 """
    if num_tokens_from_string(text, "cl100k_base") <= max_tokens:
        return [text]
    else:
        # 尝试找到合适的分割点
        mid_point = len(text) // 2
        # 确保在一个自然语言分割点进行分割（例如空格或句号后）
        while mid_point < len(text) and not text[mid_point].isspace():
            mid_point += 1

        part1 = text[:mid_point].strip() + split_suffix
        part2 = split_prefix + text[mid_point:].strip()

        # 对每部分递归调用此函数
        return split_text_to_fit_token_limit(part1, max_tokens, split_prefix,
                                             split_suffix) + split_text_to_fit_token_limit(part2, max_tokens,
                                                                                           split_prefix, split_suffix)


def process_text_to_dataframe(text, min_newlines=4):
    """ 按换行符数量分割文本，并转换为 DataFrame，分割策略为换行符数量 """
    segments = re.split(r'\n{' + str(min_newlines) + ',}', text)
    chunks = []
    embeddings = []

    for segment in segments:
        clean_segment = segment.strip()  # 清除前后空白字符
        if clean_segment:  # 确保不是空字符串
            sub_segments = split_text_to_fit_token_limit(clean_segment)
            for sub_segment in sub_segments:
                chunks.append(sub_segment)
                embeddings.append(get_embedding(sub_segment))

    df = pd.DataFrame({
        'chunk': chunks,
        'embedding': embeddings
    })
    return df


def cosine_similarity(v1, v2):
    """计算两个向量的余弦相似度"""
    return np.dot(v1, v2) / (norm(v1) * norm(v2))


# 主执行逻辑
if __name__ == "__main__":
    '''    # 读取文本文件
    text_data = load_text_file('三国演义_baihua.txt')  # 修改为你的文件路径

    total_token = num_tokens_from_string(text_data, "cl100k_base")
    print(total_token)

    # 处理文本并获取 DataFrame
    df = process_text_to_dataframe(text_data)

    # 将 DataFrame 的内容（文本块和对应的向量）保存到 CSV 文件
    df.to_csv('vectors_database.csv', index=False)'''

    # 读取向量数据库CSV 文件
    df = pd.read_csv('vectors_database.csv')
    # 假设 CSV 文件中储存向量的列名为 'embedding'
    # 将字符串转换为NumPy数组
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)

    input_query = input("输入你的问题: ")
    query_vector = get_embedding(input_query)

    # 应用余弦相似度计算每个向量与查询向量的相似度
    df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity(x, query_vector))

    # 找出相似度最高的文本块
    top_results = df.sort_values(by='similarity', ascending=False).head(10)

    # 确保按正确方式访问 DataFrame
    if not top_results.empty:
        first_result = top_results.iloc[0]  # 使用 iloc 来获取第一行
        result_text = first_result['chunk']  # 访问 'chunk' 列

        message = [{"role": "user", "content": result_text + "\n" + input_query}]
        #message = [{"role": "user", "content": input_query}]
        # 使用结果
        for response_part in chat_with_ai(message):
            print(response_part, end="")
    else:
        print("没有找到相关的结果。")
