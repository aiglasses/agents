import json
import sys
import os
import asyncio
import traceback
import uvicorn
from fastapi import APIRouter, FastAPI, Request, HTTPException
from pathlib import Path
from loguru import logger
from fastapi.responses import StreamingResponse
from typing import Dict, List, Any, Tuple, Union

root_path = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(root_path))
print(f"root_path: {root_path}")

from custom_agent_demos.token_validation import CustomMiddleware
from client_initializer import LLM_EXPERT_MAP
from response_util import to_openai_response
from util import retry_later_msg

llm_app = FastAPI()
llm_router = APIRouter()


def validate_params(body: Dict[str, Any]) -> Tuple[Union[bool, str], List, List, str, str, str]:
    stream = body.get("stream", "")
    if not stream:
        raise HTTPException(status_code=400, detail="error: stream is empty")
    messages = body.get("messages", [])
    if not messages:
        raise HTTPException(status_code=400, detail="error: messages is empty")
    tools = body.get("tools", [])
    model = body.get("model", "")
    location = body.get("location", "")
    localtime = body.get("localtime", "")
    if not model:
        raise HTTPException(status_code=400, detail="error: model is empty")
    return stream, messages, tools, model, location, localtime

if os.environ.get("ENV", "dev") != "dev":
    app.add_middleware(CustomMiddleware)


@llm_router.get("/test")
async def test():
    return {"message": "Hello world"}


# if os.environ.get("ENV", "dev") != "dev":
#     app.add_middleware(CustomMiddleware)

def stream_helper(body, llm: str):
    stream, messages, tools, model, location, localtime = validate_params(body)
    try:
        client = LLM_EXPERT_MAP[llm]
        for c in client(messages, tools, location, localtime):
            yield c
    except Exception as e:
        yield to_openai_response({"content": retry_later_msg(), "finish_reason": "stop"})
        logger.error(traceback.format_exc())


@llm_router.post("/call-qwen")
async def call_qwen(request: Request):
    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="error: request cannot be decoded to json")
    return StreamingResponse(stream_helper(body, "<qwen>"), media_type="application/json")


@llm_router.post("/call-doubao")
async def call_doubao(request: Request):
    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="error: request cannot be decoded to json")
    return StreamingResponse(stream_helper(body, "<doubao>"), media_type="application/json")


@llm_router.post("/call-deepseek")
async def call_deepseek(request: Request):
    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="error: request cannot be decoded to json")
    return StreamingResponse(stream_helper(body, "<deepseek>"), media_type="application/json")


llm_app.include_router(llm_router, prefix="/llm-expert")

if __name__ == "__main__":
    import socket
    logger.info(f"server starting on ip '0.0.0.0', port: 30001")
    uvicorn.run(
        "server:llm_app",
        host="0.0.0.0",
        port=30001,
        workers=1,
        reload=False
    )
