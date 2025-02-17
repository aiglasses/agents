# -*- encoding: utf-8 -*-
import json
from copy import deepcopy
from typing import Dict, Optional

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


def to_openai_response(chunk_obj: Dict[str, Optional[str]]) -> str:
    openai_format = deepcopy(OPENAI_RESPONSE_FORMAT)
    finish_reason = chunk_obj["finish_reason"]

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

    return "data:" + json.dumps(openai_format, ensure_ascii=False, separators=(',', ':')) + "\n"
