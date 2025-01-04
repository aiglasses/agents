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


def to_json_blob(data):
    try:
        # Try to parse the string as JSON
        json.loads(data)
        print("error: data is already JSON\n", flush=True)
        return data
    except Exception:
        pass

    if 'content' in data:
        data['content'] = data['content'].replace("\n", "").replace("\r", "")
    return json.dumps(data, ensure_ascii=False, separators=(',', ':')) + "\n"


def to_openai_response(chunk_obj: Dict[str, Optional[str]], stream: bool) -> str:
    openai_format = deepcopy(OPENAI_RESPONSE_FORMAT)
    if stream:
        delta_object = {
                    "role": "assistant",
                    "content": chunk_obj["content"],
                    "refusal": None,
                    "tool_calls": []
                }
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
        choices = [{
                "message": message_object,
                "logprobs": None,
                "finish_reason": chunk_obj["content"],
                "index": 0
            }]
        openai_format["object"] = "chat.completion"
        openai_format["choices"] = choices

    return "data:" + to_json_blob(openai_format) + "\n"
