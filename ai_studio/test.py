

import requests
from pydantic import json

url = "https://xqtd520qidong.com/v1/chat/completions"


def load_text_file(file_path):
    """ 读取整个文本文件 """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


text_data = load_text_file('RAG/三国演义_baihua.txt')  # 修改为你的文件路径

headers = {
    "Authorization": "sk-cPlT9EIGy119ra3F92CfCeAfB0C741A9Be38848a6d26B6Bd",
    "content-type": "application/json"
}
input_prompt = input("输入")
data = {
    "messages": [
        {
            "role": "user",
            "content": text_data + input_prompt,
        }
    ],
    "model": "claude-3-sonnet-20240229",
    "max_tokens_to_sample": 300,
    "stream": True
}

response = requests.post(url, headers=headers, json=data)
print(response.text)

