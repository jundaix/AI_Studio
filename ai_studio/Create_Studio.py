from ai_studio.agent import Agent
from ai_studio.functioncalling import functioncall

current_studio = None


class Studio:
    def __init__(self, name, task):
        self.name = name
        self.task = task
        self.agents = []  # 初始化 agents 为空列表
        self.current_agent = None

    def apply_agent(self, agent: Agent):
        self.agents.append(agent)
        self.current_agent = agent
        print("当前代理设置为:", self.current_agent.name)  # 打印当前代理以确认


def create_agent(studio_instance):
    name_input = input("给这个机器人起个名字\n")
    system_input = input("定义该机器人的角色与任务： \n")
    model_input = input("请选择模型 \n 1:gpt-3.5-turbo \n 2.gpt-4-0125-preview \n 3.gpt-4-turbo \n")
    if model_input == 1:
        model_input = "gpt-3.5-turbo"
    elif model_input == 2:
        model_input = "gpt-4-0125-preview"
    elif model_input == 3:
        model_input = "gpt-4-turbo"
    use_context_input = input("是否启用上下文 请只回答 True 或者 Flase \n")
    new_agent = Agent(name=name_input, system=system_input, model=model_input, use_context=use_context_input)
    studio_instance.apply_agent(new_agent)
    print("代理已创建:", new_agent.name)  # 确认代理创建


def create_studio():
    global current_studio
    name = input("请你给这个工作室起个名称\n")
    task = input("这个工作室主要用来做什么?\n")
    current_studio = Studio(name, task)
    print("初始化工作室：", current_studio.name)
    while len(current_studio.agents) == 0:
        worker_prompt_before = "当前工作室没有工作人员，请为这个工作室安排工作人员，注意要一个一个进行创建\n"
        #other_information = "当前工作室的对象名称为 current_studio"
        worker_prompt = input(worker_prompt_before)
        worker_prompt = worker_prompt + worker_prompt_before

        command = functioncall(worker_prompt)
        if command == "create_agent":
            create_agent(current_studio)
        else:
            print("出现了其他命令：" + command)
    print("工作室已创建:", current_studio.name, "有代理数量:", len(current_studio.agents))


def get_current_studio():
    return current_studio
