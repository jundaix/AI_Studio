import os
from ai_studio.Chat2AI import chat_with_ai
from ai_studio.functioncalling import functioncall


def read_file(file_path):
    """
    读取指定文件的内容并返回。
    :param file_path: 文件的完整路径或相对路径
    :return: 文件内容的字符串
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "文件未找到。"
    except Exception as e:
        return f"读取文件时发生错误：{e}"


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
    delete_lines_in_file(file_path, start_line, end_line)
    insert_content_in_file(file_path, start_line, new_content)


if __name__ == "__main__":
    #delete_lines_in_file('example.txt', 2, 4)  # 删除文件中第2行到第4行的内容
    #insert_content_in_file('example.txt', 2, "First line to insert.\nSecond line to insert.")
    #modify_lines_in_file('example.txt', 2, 5,"First line to insert.\nSecond line to insert.")

    read = read_file_with_line_numbers('example.txt')
    print(read)

    #未测试
    #command = functioncall("请你查看当前目录下的code.py，然后检查代码有没有bug")
