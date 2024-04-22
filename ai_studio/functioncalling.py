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
            "2.create_agent   这个指令用于给工作室安排机器人/工作人员/工人\n"
            "3.modify_lines_in_file  这个指令用于修改指定文件的内容 参数分别为：file_path, start_line, end_line, new_content。"
            "file_path是要修改文件包含文件名的路径，start_line和end_line用于标识需要修改的行位置，new_content是新的内容"
            "就是将file_path路径的文件的第start_line行到第end_line行的所有内容都替换new_content的内容，包含第start_line行和第end_line行"
            "本质上应该是删除从第start_line行到第end_line行的内容，然后从start_line行开始添加新内容"
            "如果new_content应为多行消息，请用换行符标识"
            "4.delete_lines_in_file 这个指令用于删除指定文件的内容 参数分别为file_path, start_line, end_line"
            "将file_path路径下的文件的第start_line到第end_line行的内容全部删除掉，包含第start_line行和第end_line行"
            "5.insert_content_in_file 这个指令用于在指定文件的指定位置插入内容 参数分别为file_path, start_line, content_to_insert"
            "将content_to_insert内容添加到file_path路径下的文件的start_line行之前的位置，如start_line为2，那么插入的内容应该从第二行开始插入，原来的第二行可以会变为第三行或者更多"
            "如果插入多行消息请用换行符标识"
            
            
            "你需要遵守的规则：\n"
            "1.你只需要回复提取后的信息就行，不要回复其他多余的话。例如输入为 创建一个工作室，你应该只回复 create_studio\n"
            "2.如果指令包含参数，指令名和参数，以及参数和参数之间用","间隔"
            "3.如果需要返回多个指令请你以换行符号进行间隔"
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
