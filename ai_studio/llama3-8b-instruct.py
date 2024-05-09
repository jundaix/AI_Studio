from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]

input_ids = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt"
).to(model.device)

tokenizer.pad_token = tokenizer.eos_token


# Use torch.inference_mode for memory and computational efficiency
with torch.inference_mode():
    while True:
        # 生成文本时传递注意力掩码参数
        outputs = model.generate(
            input_ids,
            max_new_tokens=1,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
            eos_token_id=tokenizer.eos_token_id,
            bos_token_id=tokenizer.bos_token_id,
            pad_token_id=tokenizer.pad_token_id
        )
        response = outputs[0][input_ids.shape[-1]:]
        decoded_response = tokenizer.decode(response, skip_special_tokens=True)
        print(decoded_response, end="")

        # 将生成的文本追加到输入文本的末尾作为下一次生成的输入
        input_ids = torch.cat([input_ids, response.unsqueeze(0)], dim=-1)
