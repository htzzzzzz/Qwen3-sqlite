from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print
import os

Qwen_api_key = os.getenv("QWEN_API_KEY")
# print(Qwen_api_key)

llm_cfg={
    'model': 'qwen3-235b-a22b', #可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    'model_server': 'dashscope',
    'api_key': Qwen_api_key, #'你注册的api-key'
    'generate_cfg':{
        'top_p': 0.8 # top_p越高生成的文本越多样, 范围在0-1.0之间
    }
}

bot = Assistant(
    llm=llm_cfg,
    system_message='你是一位乐于助人的小助理',
    name='智能助理'
)

messages = [] #存储历史聊天内容
while True:
    query = input('\n用户请求：输入 quit 终止对话')
    if query == 'quit':
        break
    else:
        messages.append({
            'role': 'user',
            'content': query
        })

        response = []
        response_plain_text = ''

        print('AI 回复:')
        for response in bot.run(messages=messages):
            response_plain_text = typewriter_print(response, response_plain_text)

        messages.extend(response)
