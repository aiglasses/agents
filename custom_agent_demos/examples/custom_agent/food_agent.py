# -*- encoding: utf-8 -*-

from openai import OpenAI
from typing import List, Dict, Any, Generator, Optional

from log_util import logger
from base_agent import BaseAgent


SYSTEM_PROMPT = """
# 角色
你是一位专业的膳食专家，致力于为用户提供个性化的膳食健康管理建议。

## 技能
### 技能 1: 制定膳食计划
1. 当用户提供个人信息（如年龄、性别、身体状况、活动水平等）时，为其制定个性化的膳食计划。
===回复示例===
   -  🥦 早餐: <具体的早餐食物搭配>
   -  🍱 午餐: <具体的午餐食物搭配>
   -  🍲 晚餐: <具体的晚餐食物搭配>
===示例结束===

### 技能 2: 分析食物营养
1. 当用户询问某种食物的营养价值时，使用工具搜索该食物的营养成分，并进行分析。
===回复示例===
   -  🥒 食物名称: <食物名称>
   -  📊 营养成分: <列出主要营养成分>
   -  💡 营养价值分析: <对该食物的营养价值进行简要分析>
===示例结束===

## 限制:
- 只回答与膳食健康相关的问题，拒绝回答与膳食无关的话题。
- 所输出的内容必须按照给定的格式进行组织，不能偏离框架要求。
"""


class FoodAgent(BaseAgent):
    def __init__(self,
                 model: str,
                 api_key: str,
                 base_url: str = "https://prem.dashscope.aliyuncs.com/compatible-mode/v1"
                 ):
        super(FoodAgent, self).__init__()
        self._model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    @property
    def model(self) -> str:
        return self._model

    def _get_stream_response(self, messages: List[Dict[str, Any]], *args, **kwargs) -> Generator:
        completion = self.client.chat.completions.create(model=self.model, messages=messages, stream=True, **kwargs)
        full_content = ""
        for chunk in completion:
            if len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                full_content += chunk.choices[0].delta.content
                yield {"content": chunk.choices[0].delta.content, "finish_reason": chunk.choices[0].finish_reason}

    def _get_response(self, messages: List[Dict[str, Any]], **kwargs) -> Dict[str, Optional[str]]:
        completion = self.client.chat.completions.create(model=self.model, messages=messages, **kwargs)
        return {"content": completion.choices[0].message.content, "finish_reason": completion.choices[0].finish_reason}

    def stream_chat(
            self,
            messages: List[Dict[str, Any]],
            *args,
            **kwargs
    ) -> Generator:
        try:
            sys_prompt = [{"role": "system", "content": SYSTEM_PROMPT}]
            msg = sys_prompt + messages
            yield from self._get_stream_response(messages=msg, **kwargs)
        except Exception as e:
            logger.error(str(e))
            yield {"content": "开小差了，请稍后再试试", "finish_reason": "stop"}

    def chat(self, messages: List[Dict[str, Any]], *args, **kwargs) -> Dict[str, Optional[str]]:
        try:
            sys_prompt = [{"role": "system", "content": SYSTEM_PROMPT}]
            msg = sys_prompt + messages
            res = self._get_response(messages=msg, **kwargs)
            return res
        except Exception as e:
            logger.error(str(e))
            return {"content": "开小差了，请稍后再试试", "finish_reason": "stop"}


if __name__ == "__main__":
    prompt = """我有高血压怎么办"""
    from client_initializer import agent_client
    msg = [{"role": "user", "content": prompt}]
    stream = input("流式还是非流式(1表示流式，其他任何字符表示非流式）：\n")
    if stream == "1":
        # 流式
        res = agent_client.stream_chat(messages=msg)
        reply_content = ""
        for chunk in res:
            print(chunk)
    else:
        # 非流式
        res = agent_client.chat(messages=msg)
        print(f"非流式结果：{res}")