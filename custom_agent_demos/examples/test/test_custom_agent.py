# -*- encoding: utf-8 -*-
import httpx
import json
import asyncio

async def chat_impl():
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer fsdfsfsdfsf123",
    }
    payload = {
        "model": "qwen-plus",
        "messages": [{"role": "user", "content": "膳食专家，高血压应该吃什么"}],
        "max_tokens": 512,
        "temperature": 0.5,
        "stream": True,
    }

    url = "http://localhost:30001/custom_agent/chat"
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream("POST", url, headers=headers, json=payload) as response:
                if response.status_code != 200:
                    response_text = await response.aread()
                    print(f"Request failed with status {response.status_code}: {response_text.decode()}")
                    raise Exception(f"Error {response.status_code}: {response_text.decode()}")

                async for line in response.aiter_lines():
                    if line.startswith("data:"):
                        data_str = line[len("data:"):].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            print(data)  # 打印数据或进行处理
                        except json.JSONDecodeError:
                            print(f"Invalid JSON: {data_str}")
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(chat_impl())
