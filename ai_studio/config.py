import os

MOONSHOT_API_KEY = "sk-JvoIXsJOtn6NjyKKcxmKOEPgULnpLvIGgg0laIYgIAMKqLEZ"
GPT4_API_KEY = "sk-emcpbO6oET6MH0TX72847c716eD44aB2B449B63b19A60538"
GPT3_API_KEY = "sk-a48pdCleCaMjMWzUFeE9D00c555442EfBa845c45BcF8Ef38"
GPT4o = {
    "GPT4o_API_KEY": "sk-XKWG5jLMARlWy3bN05296b0fF50344908c74C90022Ba74Cb",
    "base_url": "https://api.xiaoai.plus/v1"
}


def set_gpt4o():
    # 设置 OPENAI_API_KEY 环境变量
    os.environ["OPENAI_API_KEY"] = GPT4o["GPT4o_API_KEY"]
    # 设置 OPENAI_BASE_URL 环境变量
    os.environ["OPENAI_BASE_URL"] = GPT4o["base_url"]
