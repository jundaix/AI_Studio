from ai_studio.Chat2AI import chat_with_ai

'''from  command import xxx
Langchain  RAG 
//插件系统  command用户自拓展能力
管理员后台 搭配日志系统来用
'''


def functioncall(command_message):
    # 构造提示词，引导模型提取有用信息
    prompt = (
            "目前已有的指令：\n"
            "1.create_studio  这个指令没有参数 这个指令跟创建工作室或者工作环境等有关\n"
            "2.create_agent   这个指令用于给工作室安排机器人/工作人员/工人"
            "你需要遵守的规则：\n"
            "1.你只需要回复提取后的信息就行，不要回复其他多余的话。例如输入为 创建一个工作室，你应该只回复 create_studio\n"
            "2.只能回复一个指令，假如输入信息可能跟多个指令相关，选择最可能符合用户意图的"
            "需要转化的指令信息为：\n" + command_message
    )
    # 调用模型
    messages = [
        {"role": "system", "content": "你的任务是 将一段自然语言形式的指令转化为指定格式的指令输出\n"},
        {"role": "user", "content": prompt}
    ]
    response = " "
    for response_part in chat_with_ai(messages, "gpt-3.5-turbo"):
        response += response_part  # 在外部累积完整的响应内容

    # 获取模型的回复，这里假定 response 是一个字典，并且结构正确
    command_info = response.strip()  # 这里根据返回的 JSON 结构来访问 content
    # 执行指令
    return command_info


'''def execute_command(command_name: str):
    if command_name == "create_studio":
        create_studio()
    else:
        print("没找到命令："+command_name)'''
