from ai_studio.agent import Agent
from ai_studio.functioncalling import functioncall

current_studio = []

class studio:
    def __init__(self, name, task):
        self.name = name
        self.task = task
        self.agents = []  # 初始化 agents 为空列表
        self.current_agent = []
    def apply_agent(self,agent:Agent):
        self.agents.append(agent)
        self.current_agent = agent

def create_agent(studio):
    name_input = input("给这个机器人起个名字\n")
    system_input = input("定义该机器人的角色与任务： \n")
    model_input = input("请选择模型 gpt-3.5-turbo  or  gpt-4-0125-preview \n")
    use_context_input = input("是否启用上下文 请只回答 Ture 或者 Flase \n")
    new_agent = Agent(name = name_input,system=system_input,model = model_input,use_context = use_context_input)
    studio.apply_agent(new_agent)


def create_studio():
    name = input("请你给这个工作室起个名称\n")
    task = input("这个工作室主要用来做什么?\n")
    current_studio = studio(name,task)
    if(len(current_studio.agents) == 0):
        worker_prompt_before = "当前工作室没有工作人员，请为这个工作室安排工作人员，注意要一个一个进行创建\n"
        #other_information = "当前工作室的对象名称为 current_studio"
        worker_prompt = input(worker_prompt_before)
        worker_prompt = worker_prompt + worker_prompt_before

        command = functioncall(worker_prompt)
        if command == "create_agent":
            create_agent(current_studio)
        else:
            print("出现了其他命令："+command)

    
