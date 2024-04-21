import os

def read_file(file_path):
    """ 读取文件内容并返回 """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    """ 将内容写入文件 """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def create_file(file_path):
    """ 创建一个新文件 """
    with open(file_path, 'w', encoding='utf-8'):
        pass

def edit_file_content(file_path, mode, original_text, new_text=None, position=None):
    """ 编辑文件内容，包括添加、删除和修改文本 """
    # 读取原始文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 根据不同的模式执行操作
    if mode == 'add' and position is not None:
        # 插入文本
        pos = content.find(original_text)
        if pos != -1:
            pos += position
            content = content[:pos] + new_text + content[pos:]
    elif mode == 'delete':
        # 删除文本
        content = content.replace(original_text, '')
    elif mode == 'modify':
        # 修改文本
        content = content.replace(original_text, new_text)
    else:
        raise ValueError("Invalid mode or parameters")

    # 将修改后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# 示例用法
edit_file_content('example.txt', 'add', 'specific position', 'Hello, ', position=15)
edit_file_content('example.txt', 'delete', 'remove this text')
edit_file_content('example.txt', 'modify', 'old text', 'new text')



# 示例使用
file_content = read_file('/path/to/your/directory/example.txt')  # 读取文件
write_file('/path/to/your/directory/example.txt', 'Hello, world!')  # 写入内容
create_file('/path/to/your/directory/newfile.txt')  # 创建新文件
