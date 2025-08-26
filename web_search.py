import os

import httpx
from mcp.server import FastMCP
from google import genai

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY", "")
if api_key == "":
    exit(1)

# # 初始化 FastMCP 服务器
app = FastMCP('web-search')

api_key_gemini = os.getenv("API_KEY_GEMINI", "")
if api_key_gemini == "":
    exit(1)

client = genai.Client(api_key=api_key_gemini)

@app.tool()
async def web_search(query: str) -> str:
    """
    搜索互联网内容

    Args:
        query: 要搜索内容

    Returns:
        搜索结果的总结
    """

    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://open.bigmodel.cn/api/paas/v4/tools',
            headers={'Authorization': api_key},
            json={
                'tool': 'web-search-pro',
                'messages': [
                    {'role': 'user', 'content': query}
                ],
                'stream': False
            }
        )

        res_data = []
        for choice in response.json()['choices']:
            for message in choice['message']['tool_calls']:
                search_results = message.get('search_result')
                if not search_results:
                    continue
                for result in search_results:
                    res_data.append(result['content'])

        return '\n\n\n'.join(res_data)


@app.tool()
async def web_search_gemini(query: str) -> str:
    """
    搜索互联网内容

    Args:
        query: 要搜索内容

    Returns:
        搜索结果的总结
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query
    )

    return response.text if response.text else "nothing"

if __name__ == "__main__":
    app.run(transport='stdio')