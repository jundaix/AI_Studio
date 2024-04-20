import openai
from ai_studio.agent import Agent
from ai_studio.functioncalling import functioncall
from ai_studio.Create_Studio import create_studio,current_studio
# 设置你的OpenAI API密钥
openai.api_key = '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'

# 示例调用
#gpt-4-0125-preview
#gpt-3.5-turbo
#gpt-4-turbo
start_prompt_before = "当前没有工作室，是否要创建一个\n"
start_prompt = input(start_prompt_before)
start_prompt = start_prompt + start_prompt_before
start_command = functioncall(start_prompt)
if start_command == "create_studio":
    create_studio()
else:
    print("出现了其他命令："+start_command)

# 创建Robot实例

while 1:
    # 开始对话
    user_input = input("用户： ")
    print("助手：", current_studio.current_agent.send_message(user_input))

'''
现在已经完成了Agent的设计

预期的整体效果：
机器人自己的功能：
记忆————上下文管理、冗余的记忆清除、暂时用不到的记忆暂存。     
Tools————造一些可以供机器人调用的工具
Action——————调用其他小模型的能力、联网、执行指令
Planning——————怎么规划思维模式

假如我想做的是一个AI工作站
我需要有一个写代码的 根据要求生成代码，它需要知道总目标是什么，还需要知道当前的子目标是什么，还需要知道当前代码
我还需要一个改代码的 根据当前代码和目标，以及当前的小目标，还有代码出现的问题，对代码进行修改
我还需要一个架构师   把一个项目分为很多个小步骤执行，如果小步骤还能分那就继续分解。
我还需要一个项目管理者 记录当前的项目进展，发布子任务给打工人。

需要的能力：
1.将代码内容写入。
2.执行代码
3.可以联网下载，或者是执行pip install这样的指令
4.读取错误信息
5.Google Search

完成一个项目的流程：
首先我要得到项目要求。然后根据项目要求制定策略。
-----------军师团---------      曹操举兵伐袁术 可以参考荀彧、程昱等三人给曹操制定方案的场景 建议主公用之 建议主公杀之 建议主公先杀之再用之
制定策略可以让多个机器人一起参与，如果能用其他的大模型如 Gemini1.5、Clude、文心一言等可能会更好
然后根据它们提出的想法，再进行一个融合得到几个集百家之长的新方案。
然后投票选出最可能是有效的方案。

得到方案之后再进行任务的肢解。step by step
然后应该有一个项目


Tools:
创建机器人，安排协作对象
可以创建机器人，给机器人安排工作。可以看到它们的工作状态和内容
可以安排多个机器人协作。
可以记录机器人的任务完成状态。比如进展到了第几步。

UI可以看到整体的信息 包括机器人的数量  花费的token  
可以看见机器人的工作内容
'''

'''
Awakening 22:41:57
从现在开始，你是一名指令发布者，你的作用就是根据当前的情况发布指令。
目前可供你发布的指令有：Move   参数有三个 ，分别是i、x 、y，都是整数类型,代表让机器人i移动到点(x,y)位置；
  ship ，参数有两个，分别是i 、j，也都是整数类型，代表让船i移动到港口j。 
  请你时刻记住除了跟发布指令相关的内容都不要表达。
  还有就是你输出的格式为。  Move i x y。如让机器人5移动到点100，100位置，你的输出应该为：Move 5 100 100 。  
  同理让船7移动到港口2。输出为 ship 7 2 。            现
  在我想要让机器人4到达188，175位置，请你输出指令。

  Move 4 188 175

Awakening 22:42:41
从现在开始，你是一名指令发布者，你的作用就是根据当前的情况发布指令。
目前可供你发布的指令有：Move   参数有三个 ，分别是i、x 、y，都是整数类型,代表让机器人i移动到点(x,y)位置；  
ship ，参数有两个，分别是i 、j，也都是整数类型，代表让船i移动到港口j。 请你时刻记住除了跟发布指令相关的内容都不要表达。
还有就是你输出的格式为。 Move i x y。如让机器人5移动到点100，100位置，你的输出应该为：Move 5 100 100 。  
同理让船7移动到港口2。输出为 ship 7 2 。            
现在我想要让船6到达港口8，请你输出指令。

ship 6 8
'''