# -*- encoding: utf-8 -*-
import json
from types import SimpleNamespace
from copy import deepcopy
from typing import Dict, Any, Optional

OPENAI_RESPONSE_FORMAT = {
    "id": "",
        "choices": [],
        "created": 0,
        "model": "",
        "service_tier": None,
        "system_fingerprint": "",
        "object": "",
        "usage": None,
}


def to_openai_response(chunk_obj: Dict[str, Optional[str]], stream: bool = True) -> str:
    openai_format = deepcopy(OPENAI_RESPONSE_FORMAT)
    finish_reason = chunk_obj["finish_reason"]
    if stream:
        delta_object = {
                    "role": "assistant",
                    "content": chunk_obj["content"],
                    "refusal": None,
                    "tool_calls": []
                }
        if finish_reason == "tool_calls":
            delta_object["tool_calls"] = chunk_obj["tool_calls"]
        choices = [{
                "delta": delta_object,
                "logprobs": None,
                "finish_reason": chunk_obj["finish_reason"],
                "index": 0
            }]
        openai_format["choices"] = choices
        openai_format["object"] = "chat.completion.chunk"
    else:
        message_object = {
                    "role": "assistant",
                    "content": chunk_obj["content"],
                    "refusal": None,
                    "tool_calls": [],
                    "audio": None
                }
        if finish_reason == "tool_calls":
            message_object["tool_calls"] = chunk_obj["tool_calls"]
        choices = [{
                "message": message_object,
                "logprobs": None,
                "finish_reason": chunk_obj["content"],
                "index": 0
            }]
        openai_format["object"] = "chat.completion"
        openai_format["choices"] = choices
    return "data:" + json.dumps(openai_format, ensure_ascii=False, separators=(',', ':')) + "\n"
