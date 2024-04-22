import os
from ai_studio.Chat2AI import chat_with_ai
from ai_studio.functioncalling import functioncall
from ai_studio.agent import Agent
import re

def read_file_with_line_numbers(file_path):
    """
    读取指定文件的内容，并在每行前添加行号。
    :param file_path: 文件的完整路径或相对路径
    :return: 每行内容前带行号的字符串
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # 使用枚举来获取每行的索引和内容，格式化字符串以包括行号
        return ''.join([f"第{idx + 1}行: {line}" for idx, line in enumerate(lines)])
    except FileNotFoundError:
        return "文件未找到。"
    except Exception as e:
        return f"读取文件时发生错误：{e}"


def delete_lines_in_file(file_path, start_line, end_line):
    """ 删除文件中从行N到行M的所有内容 """
    try:
        # 将行号从字符串转换为整数
        start_line = int(start_line)
        end_line = int(end_line)
    except ValueError:
        raise ValueError("Start line and end line must be integers.")

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 确保指定的行号在文件行数范围内
    if start_line < 1 or end_line > len(lines):
        raise IndexError("Line numbers out of range")
    # 删除指定的行
    del lines[start_line - 1:end_line]

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def insert_content_in_file(file_path, start_line, content_to_insert):
    """ 在指定行开始添加内容（支持多行） """
    try:
        # 将行号从字符串转换为整数
        start_line = int(start_line)
    except ValueError:
        raise ValueError("Start line must be an integer.")

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 确保指定的行号在文件行数加一的范围内（允许在文件末尾添加新行）
    if start_line < 1 or start_line > len(lines) + 1:
        raise IndexError("Line number out of range")

    # 分割多行内容为列表，每项为一行
    insert_lines = content_to_insert.split('\n')
    # 将每项添加换行符并准备插入
    insert_lines = [line + '\n' for line in insert_lines]

    # 插入内容到指定位置
    lines[start_line - 1:start_line - 1] = insert_lines

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def modify_lines_in_file(file_path, start_line, end_line, new_content):
    """ 修改文件中第N行到第M行的内容 """
    try:
        # 将行号从字符串转换为整数
        start_line = int(start_line)
        end_line = int(end_line)
    except ValueError:
        raise ValueError("Start line and end line must be integers.")

    delete_lines_in_file(file_path, start_line, end_line)
    insert_content_in_file(file_path, start_line, new_content)


def parse_function_call(input_str):
    """
    解析包含函数名和参数的字符串。
    :param input_str: 格式为 "函数名,参数1,参数2,...,参数n" 的字符串
    :return: 字典，包含函数名和参数列表
    """
    parts = input_str.split(',')
    function_name = parts[0]  # 第一个元素是函数名
    function_name = function_name.replace(" ", "")
    parameters = parts[1:]  # 剩余的元素是参数列表
    parameters[0] = parameters[0].replace(" ", "")
    return {
        'function_name': function_name,
        'parameters': parameters
    }


def extract_code(markdown_code_block):
    """
    Extracts the code from a markdown code block delimited by triple backticks.

    :param markdown_code_block: A string containing a Markdown code block
    :return: The code inside the Markdown code block
    """
    # Use regular expression to match content inside triple backticks
    match = re.search(r'```(?:python)?\s*(.*?)\s*```', markdown_code_block, re.DOTALL)
    if match:
        return match.group(1)  # Return the captured group containing the code
    else:
        return None  # Return None if no match is found

if __name__ == "__main__":
    #delete_lines_in_file('example.txt', 2, 4)  # 删除文件中第2行到第4行的内容
    #insert_content_in_file('example.txt', 2, "First line to insert.\nSecond line to insert.")
    #modify_lines_in_file('example.txt', 2, 5,"    if x > 0:\n        return x + y\n    else:\n        return x - y")

    command = functioncall("请你查看当前目录下的code.txt的内容")
    debugger = Agent(name="debugger",
                     system="从现在开始你是一名debugger工程师，我会发给你标识了行号的代码内容，请你对代码有问题的地方进行修改",
                     model="gpt-4-turbo")

    result = parse_function_call(command)
    print("result1:", result)
    if result['function_name'] == "read_file_with_line_numbers":
        file_message = read_file_with_line_numbers(result['parameters'][0])
        print("file_message \n", file_message)

        send_message = "这是我的code.txt文件的内容，你不需要调用阅读函数了，我已经帮你读取了，请你对这段代码进行debug"\
                       "可能需要调用修改文件内容的函数，此外请你返回的内容只包括代码和注释，代码中标识的第几行，是我为了便于你理解的"\
                        "并且你需要回复对xx文件的xx行到xx行的内容修改为xxxxx,如果多行用换行符标识,一定要回复对具体哪个文件进行的修改！"\
                        "另外注意你回复修改文件的第xx行到xx行时，要针对的是修改之前的情况，如果原来的文件只有两行，你不可以回复超过2的行数"\
                        "此外修改这种python文件要注意缩进对齐"\
                        "我的代码为："
        debugger_result = debugger.send_message(send_message + file_message)
        print("debugger_result ", debugger_result)

        command2 = functioncall(send_message + file_message + "解决方案为:"+debugger_result)
        result2 = parse_function_call(command2)
        print("result2:", result2)

        if result2['function_name'] == "modify_lines_in_file":
            result2['parameters'][3] = extract_code(result2['parameters'][3])

            try:
                print(f"{result2['function_name']}('{result2['parameters'][0]}',{result2['parameters'][1]}, {result2['parameters'][2]},result2['parameters'][3])")
                eval(f"{result2['function_name']}('{result2['parameters'][0]}',{result2['parameters'][1]}, {result2['parameters'][2]},result2['parameters'][3])")
            except Exception as e:
                print(e)
                raise e
            '''modify_lines_in_file(result2['parameters'][0], result2['parameters'][1], result2['parameters'][2],
                                 result2['parameters'][3])'''
