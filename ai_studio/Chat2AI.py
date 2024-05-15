from openai import OpenAI
import tiktoken
from config import *

def load_text_file(file_path):
    """ 读取整个文本文件 """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


#流式输出
def chat_with_ai(messages, model="gpt-4o"):
    global client
    if model == "moonshot-v1-128k":
        client = OpenAI(
            api_key=MOONSHOT_API_KEY,
            base_url="https://api.moonshot.cn/v1",
        )
    elif model == "gpt-3.5-turbo":
        client = OpenAI(
            api_key=GPT3_API_KEY
        )
    elif model == "gpt-4-1106-preview":
        client = OpenAI(
            api_key=GPT4_API_KEY
        )
    elif model == "gpt-4o":
        set_gpt4o()
        client = OpenAI(
        )
    else:
        client = OpenAI()
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content  # 使用 yield 而不是 return


# 使用示例
'''text_data = load_text_file('RAG/三国演义_baihua.txt')  # 修改为你的文件路径

input_prompt = input("输入你的问题: ")
message = [{"role": "user", "content": " " + input_prompt}]
for response_part in chat_with_ai(message):
    print(response_part, end="")'''
