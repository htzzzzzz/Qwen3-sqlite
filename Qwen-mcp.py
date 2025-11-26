from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print
import os
Qwen_api_key = os.getenv("QWEN_API_KEY")
def init_agent_service():
    llm_cfg={
        'model': 'qwen3-235b-a22b',
        'model_server': 'dashscope',
        'api_key': Qwen_api_key, #'你的api_key',
        'generate_cfg':{
            'top_p': 0.8
        }
    }

    # 定义MCP服务配置，优点类似Function Calling调用的JSON Schema格式
    tools = [{
        "mcpServers": {
            "sqlite": {
                "command": "mcp-server-sqlite",
                "args": [
                    "--db-path",
                    "test.db"
                ]
            }
        }
    }]

    bot = Assistant(
        llm=llm_cfg,
        name='数据库管理员',
        description='你是一位数据库管理员，具有对本地数据库的增删改查能力',
        system_message='你扮演一个数据库助手，你具有查询数据库的能力',
        function_list=tools,
    )

    return bot

def run_query(query=None):
    # 定义数据库助手
    bot = init_agent_service()

    # 执行对话逻辑
    messages = []
    messages.append({'role': 'user', 'content': [{'text': query}]})

    # 跟踪前一次的输出，用于增量打印
    previous_text = ""

    print('数据库管理员: ', end='', flush=True)

    for response in bot.run(messages):
        previous_text = typewriter_print(response, previous_text)

if __name__ == '__main__':
    query = '帮我创建一个学生表,表名是students,包含id, name, age, gender, score字段,然后插入一条数据,id为1,name为张三,age为20,gender为男,score为95'
    run_query(query)
