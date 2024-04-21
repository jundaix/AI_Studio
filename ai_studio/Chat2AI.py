from openai import OpenAI

client = OpenAI(
    api_key="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",  # 替换为你的API密钥
)


def chat_with_ai(messages, model="gpt-4-turbo"):
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content  # 使用 yield 而不是 print


'''# 使用示例
for response_part in chat_with_ai("user", "用Verilog写FIFO代码"):
    print(response_part, end="")'''
