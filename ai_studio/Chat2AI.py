import os

os.environ["OPENAI_API_KEY"] = "sk-emcpbO6oET6MH0TX72847c716eD44aB2B449B63b19A60538"

os.environ["OPENAI_BASE_URL"] = "https://gtapi.xiaoerchaoren.com:8932/v1"

from openai import OpenAI

client = OpenAI()


#流式输出
def chat_with_ai(messages, model="gpt-4-1106-preview"):
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content  # 使用 yield 而不是 print


# 使用示例
'''input_query = input("输入你的问题: ")
message = [{"role": "user", "content": input_query}]
for response_part in chat_with_ai(message):
    print(response_part, end="")'''
