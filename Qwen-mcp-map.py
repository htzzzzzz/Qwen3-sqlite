from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print
import os
Qwen_api_key = os.getenv("QWEN_API_KEY")
Firecrawl_API_KEY = os.getenv("Firecrawl_API_KEY")
GDMAP_API_KEY = os.getenv("GDMAP_API_KEY")
def init_agent_service():
    llm_cfg = {
        'model': 'qwen3-235b-a22b',
        'model_server': 'dashscope',
        'api_key': Qwen_api_key,#'你注册的百炼 api key',
        'generate_cfg': {
            'top_p': 0.8
        }
    }

    tools = [{
        "mcpServers": {
            "firecrawl-mcp": {
                "command": "npx",
                "args": ["-y", "firecrawl-mcp"],
                "env": {
                    "FIRECRAWL_API_KEY": Firecrawl_API_KEY,#"你注册的firecrawl api key"
                },
            },

            "amap-mcp-server": {
                "command": "npx",
                "args": [
                    "-y",
                    "@amap/amap-maps-mcp-server"
                ],
                "env": {
                    "AMAP_MAPS_API_KEY": GDMAP_API_KEY,#"你注册的高德地图api key"
                }
            }
        },
    },]

    system = """
            你是一个规划师和数据分析师 \
                你可以调用高德地图规划旅行路线，同时可以提取网页信息进行数据分析
            """

    bot = Assistant(
        llm=llm_cfg,
        name='智能助理',
        description='具备查询高德地图、提取网页信息、数据分析的能力',
        system_message=system,
        function_list=tools,
    )

    return bot
def run_query(query=None):
    # 定义智能助手
    bot = init_agent_service()

    from qwen_agent.gui import WebUI

    chatbot_config = {
        'prompt.suggestions': [
            "https://github.com/orgs/QwenLM/repositories 提取这一页的Markdown 文档，然后绘制一个柱状图展示每个项目的收藏量",
            '帮我查询从故宫去颐和园的路线'
        ]
    }
    WebUI(
        bot,
        chatbot_config=chatbot_config,
    ).run()

if __name__ == '__main__':
    run_query()
