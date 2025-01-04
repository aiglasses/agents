import os
import uvicorn
from fastapi import APIRouter, FastAPI, Request
from loguru import logger
from fastapi.responses import StreamingResponse
from typing import Dict, List


from token_validation import CustomMiddleware
from base_agent import BaseAgent
from client_initializer import agent_client
from response_util import to_openai_response

app = FastAPI()
router = APIRouter()


def validate_params(request: Request) -> None:
    # todo
    pass


@router.get("/test")
async def test():
    return {"message": "Hello ShargeAI"}


if os.environ.get("ENV", "dev") != "dev":
    app.add_middleware(CustomMiddleware)


def stream_helper(client: BaseAgent, messages: List[Dict[str, str]], **kwargs):
    try:
        for chunk_obj in client.stream_chat(messages=messages, **kwargs):
            res = to_openai_response(chunk_obj=chunk_obj, stream=True)
            logger.info(f"返回结果：{res}")
            yield res
    except Exception as e:
        logger.error(str(e))
        yield to_openai_response(chunk_obj={"content": "抱歉，网络开小差了", "finish_reason": "stop"}, stream=True)


def helper(client: BaseAgent, messages: List[Dict[str, str]], **kwargs):
    try:
        res = client.chat(messages=messages, **kwargs)
        res = to_openai_response(chunk_obj=res, stream=False)
        logger.info(f"返回结果：{res}")
        return res
    except Exception as e:
        logger.error(str(e))
        return to_openai_response(chunk_obj={"content": "抱歉，网络开小差了", "finish_reason": "stop"}, stream=False)


@router.post("/chat")
async def chat(request: Request):
    validate_params(request)
    try:
        body = await request.json()
        stream = body.pop("stream")
        messages = body.pop("messages")
        expert = body.pop("model")
        logger.info(f"【入参】\n：{body}")
        if stream:
            return StreamingResponse(stream_helper(agent_client, messages, **body), media_type="application/json")
        else:
            return helper(agent_client, messages, **body)

    except Exception as e:
        logger.error(str(e))
        raise e

app.include_router(router, prefix="/custom_agent")

if __name__ == "__main__":
    import socket
    logger.info(f"server starting on ip: 8.153.78.47, port: 30000")
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=30001,
        workers=1,
        reload=True
    )