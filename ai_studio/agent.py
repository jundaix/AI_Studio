from ai_studio.Chat2AI import chat_with_ai
import tiktoken


#创建一个类 Agent类
#类的内容有 任务system  还有模型选择 上下文管理函数 任务状态函数 
class Agent:
    def __init__(self, name, system, model="gpt-3.5-turbo", use_context=True):
        self.name = name
        self.system = system
        self.model = model
        self.use_context = use_context
        self.conversation_history = [{"role": "system", "content": system}]

    def manage_context(self, role, content):
        if self.use_context:
            self.conversation_history.append({"role": role, "content": content})

    def clean_context(self):
        # 将当前对话历史转换为文本形式
        context_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history])
        # 构造提示词，引导模型提取有用信息
        prompt = (
                "你需要遵守的规则：\n"
                "1. 完整去除掉开始的system的内容，因为我后续会重新拼接。\n"
                "2. 把上下文中无用的、重复的信息去除掉,提取并摘要化针对当前的任务的真正高效和有用的信息。\n"
                "3. 将这段会话的时候整理为更符合user角色的内容，如有些内容是assitant"
                "给出的解决方案，你要解释为对于什么问题我提出了什么解决方案。总的来说就是你要明确你是一个提问者的角色，你的目的就是给出更多的信息让对方去理解\n"
                "4. 你只需要回复提取后的信息就行，不要回复其他多余的话。\n"
                "需要提取的信息为：\n" + context_text
        )
        # 调用模型
        messages = [
            {"role": "system", "content": "你的任务是 根据以下对话历史，提取与当前任务相关的高效和有用信息\n"},
            {"role": "user", "content": prompt}
        ]
        response = " "
        for response_part in chat_with_ai(messages, self.model):
            response += response_part  # 在外部累积完整的响应内容

        # 假设模型返回的文本是提取后的有用信息
        extracted_info = response.strip()  # 直接处理累积的字符串，不需要解析JSON

        # 重构对话历史
        self.conversation_history = [{"role": "system", "content": self.system}]
        if extracted_info:  # 如果有提取的信息，作为新的更新加入
            self.conversation_history.append({"role": "user", "content": extracted_info})

    def count_message_tokens(self, messages: list[dict[str, str]]) -> int:
        # 使用 count_message_tokens 计算当前对话历史的token数量
        try:
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        if self.model == "gpt-3.5-turbo":
            # !Note: gpt-3.5-turbo may change over time.
            # Returning num tokens assuming gpt-3.5-turbo-0301.")
            tokens_per_message = (
                4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            )
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif self.model == "gpt-4-0125-preview":
            # !Note: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
            tokens_per_message = 3
            tokens_per_name = 1
        else:
            raise NotImplementedError(
                f"num_tokens_from_messages() is not implemented for model {model}.\n"
                " See https://github.com/openai/openai-python/blob/main/chatml.md for"
                " information on how messages are converted to tokens."
            )
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens

    def count_string_tokens(string: str, model_name: str) -> int:
        """
        Returns the number of tokens in a text string.

        Args:
            string (str): The text string.
            model_name (str): The name of the encoding to use. (e.g., "gpt-3.5-turbo")

        Returns:
            int: The number of tokens in the text string.
        """
        encoding = tiktoken.encoding_for_model(model_name)
        return len(encoding.encode(string))

    def send_message(self, user_input):
        self.manage_context("user", user_input)

        ai_reply = " "
        for response_part in chat_with_ai(self.conversation_history, self.model):
            ai_reply += response_part  # 在外部累积完整的响应内容

        self.manage_context("assistant", ai_reply)
        if self.count_message_tokens(self.conversation_history) > 10240:
            self.clean_context()

        return ai_reply
