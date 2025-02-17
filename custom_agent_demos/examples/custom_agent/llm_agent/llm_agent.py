# -*- encoding: utf-8 -*-

import traceback
import json
import sys
import os

from volcenginesdkarkruntime import Ark
from openai import OpenAI
from loguru import logger
from copy import deepcopy
from typing import Dict, Any, Optional, List
from pathlib import Path

root_path = Path(__file__).parent.parent.parent.parent.parent.parent
sys.path.insert(0, str(root_path))

from util import retry_later_msg, read_config
from response_util import to_openai_response

config = read_config()


LLM_CONFIGS = {
    "<qwen>": {
        "client_class": OpenAI,
        "api_key": config["ali"]["apiKey"],
        "base_url": config["ali"]["addr"],
        "vl_base_url": config["ali"]["addr"],
        "txt_model": config["ali"]["txt1"]["large"],
        "vl_model": config["ali"]["vl1"]["small"],
    },
    "<doubao>": {
        "client_class": Ark,
        "api_key": config["volc"]["apiKey"],
        "base_url": config["volc"]["addr"],
        "vl_base_url": config["volc"]["addr"],
        "txt_model": config["volc"]["txt1"]["large"],
        "vl_model": config["volc"]["vl1"]["small"],
    },
    "<deepseek>": {
        "client_class": Ark,
        "api_key": config["volc"]["apiKey"],
        "base_url": config["volc"]["addr"],
        "txt_model": config["volc"]["txt2"]["large"],
        "vl_model": "",
    }
}


def get_store_simple_llm_client(llm_name: str, key="txt"):
    try:
        assert llm_name in LLM_CONFIGS, f"Unsupported LLM: {llm_name}"
        llm_config = LLM_CONFIGS[llm_name]
        assert llm_config, f"【llm agent】Missing configuration for LLM: {llm_name}"
        if key == "txt":
            return llm_config["client_class"](
                api_key=llm_config["api_key"],
                base_url=llm_config["base_url"]
            )
        elif key == "vl":
            return llm_config["client_class"](
                api_key=llm_config["api_key"],
                base_url=llm_config["vl_base_url"]
            )
    except Exception as e:
        logger.error(traceback.format_exc())
        return


class BaseLlmExpert(object):
    def __init__(self, llm_name: str):
        self.client = get_store_simple_llm_client(llm_name)
        self.vl_client = get_store_simple_llm_client(llm_name, key="vl")
        self.llm_name = llm_name

    def _call(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]]):
        try:
            for chunk_obj in self.stream_chat(messages=messages, tools=tools):
                res = to_openai_response(chunk_obj=chunk_obj)
                logger.info(f"stream result: {res}")
                yield res
        except Exception as e:
            logger.error(traceback.format_exc())
            yield to_openai_response(chunk_obj={"content": retry_later_msg(), "finish_reason": "stop"})

    def __call__(self, messages: List[Dict[str, str]], tools):
        yield from self._call(messages, tools)

    def stream_chat(
            self,
            messages: List[Dict[str, Any]],
            tools: Optional[List[Dict[str, Any]]] = None
    ):
        try:
            if self.client is None:
                yield {"content": retry_later_msg(), "finish_reason": "stop"}
                logger.error(f"【llm agent】llm client is None，please configure `LLM_CONFIGS`")
                return

            # deepseek暂不支持视觉信息
            if self.vl_client is None and messages and isinstance(messages[0]["content"], list):
                yield {"content": "对不起，我暂时还不支持视觉信息,您可以接着问我其他问题", "finish_reason": "stop"}
                logger.warning(f"【llm agent】not supported vision request for deepseek")
                return

            if messages and isinstance(messages[-1]["content"], list):
                # 如果已经是图片，忽略tools
                client = self.vl_client
                model = LLM_CONFIGS[self.llm_name]["vl_model"]
                tools = []
            else:
                client = self.client
                model = LLM_CONFIGS[self.llm_name]["txt_model"]

            if not tools:
                completion = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True,
                )
            else:
                if self.llm_name == "<deepseek>":
                    # deepseek不支持function call
                    completion = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        stream=True,
                    )
                else:
                    completion = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        stream=True,
                        tools=tools
                    )

            if not completion:
                yield {"content": retry_later_msg(), "finish_reason": "stop"}
                logger.error(f"【llm agent】{self.llm_name} model return None")
                return

            reply_content = ""
            for chunk in completion:
                if len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                    reply_content += chunk.choices[0].delta.content
                    yield {"content": chunk.choices[0].delta.content, "finish_reason": chunk.choices[0].finish_reason}
            logger.info(f'llm reply: {reply_content}')
        except Exception as e:
            yield {"content": retry_later_msg(), "finish_reason": "stop"}
            logger.error(traceback.format_exc())
