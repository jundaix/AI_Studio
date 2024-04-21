from ai_studio.Chat2AI import chat_with_ai
from ai_studio.agent import Agent


class Manager(Agent):
    def __init__(self):
        # 初始化Manager类时同时初始化父类Agent
        super().__init__()

    def main_task(self, task):
        # 这里可以定义如何使用GPT-4来分解子任务
        print("分解任务：", task)
        # 假设我们使用GPT-4来处理和分解任务
        # 你可以调用GPT-4的API来实现具体的任务分解
        response = self.use_gpt4(task)
        return response

    def use_gpt4(self, task):
        # 这里是调用GPT-4的模拟例子
        # 实际上你需要通过OpenAI的API来实现
        print("使用GPT-4处理任务：", task)
        return "任务分解结果"
