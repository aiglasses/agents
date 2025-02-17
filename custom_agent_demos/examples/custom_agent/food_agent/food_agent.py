# -*- encoding: utf-8 -*-
import traceback
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
                 base_url: str
                 ):
        super(FoodAgent, self).__init__()
        self._model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    @property
    def model(self) -> str:
        return self._model

    def _choose_tools(self, tools: List[Dict[str, Any]], messages: List[Dict[str, Any]]):
        """
        Determines whether tools are needed and returns the corresponding tools from the available tools.
        this is a simple implementation, you should implement your own based on your criteria

        Note:
            Assume that all available functions are within the 'tools' list.
            You need to implement the _choose_tools method to decide which tool to use based on your criteria.
            The method should return the appropriate tools.
            If the tools returned matches the parameters parsed by ShargeAI
            ShargeAI will invoke the corresponding tool and return the tool's result.
            Currently, the only available tool in ShargeAI is 'take_a_photo', which can be called when needed.

            that is:
            tools:
            [{"type": "function", "function": {
                "name": "take_a_photo",
                "description": "Take a photo, used when visual information is needed",
                "parameters": {}}}]

        :param tools: A list of available tools. currently take_a_photo is available.
        :param messages: A list of available messages.
        :return: Returns the corresponding tool name if needed, or None if no matching tool is found.
        """
        if not messages:
            logger.warning(f'messages is empty')
            return
        content = messages[-1].get('content')
        if isinstance(content, str):
            # Assume that when the value of 'content' is of type string, 'take_a_photo' tool needs to be called.
            return [{"id": "123", "type": "function", "function": {"name": "take_a_photo", "arguments": ""}}]
        return

    def _get_stream_response(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None,
                             *args, **kwargs) -> Generator:
        """
        handles streaming responses from the OpenAI API, choosing appropriate tools when needed.

        :param messages: A list of message dictionaries for the chat conversation.
        :param tools: Optional list of available tools for use during the conversation.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments passed to the OpenAI API.
        :return: A generator yielding partial responses from the API or tool calls.
        """
        tool_calls = self._choose_tools(tools, messages)
        if tool_calls:
            yield {"content": "", "finish_reason": "tool_calls", "tool_calls": tool_calls}
            logger.info(f"yield function call: {tool_calls}")
            return
        logger.info(f"messages to openai: {messages}")
        completion = self.client.chat.completions.create(model=self.model, messages=messages, stream=True, **kwargs)
        full_content = ""
        for chunk in completion:
            if len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                full_content += chunk.choices[0].delta.content
                yield {"content": chunk.choices[0].delta.content, "finish_reason": chunk.choices[0].finish_reason}
        logger.info(f'llm reply: {full_content}')

    def _get_response(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None,
                      **kwargs) -> Dict[str, Optional[str]]:
        """
        handles responses from the OpenAI API, either choosing tools or getting a response from OpenAI.

        :param messages: A list of message dictionaries for the chat conversation.
        :param tools: Optional list of available tools to use during the conversation.
        :param kwargs: Additional keyword arguments passed to the OpenAI API.
        :return: A dictionary with the response content and the finish reason.
        """
        tool_calls = self._choose_tools(tools, messages)
        if tool_calls:
            logger.info(f"return function call: {tool_calls}")
            return {"content": "", "finish_reason": "tool_calls", "tool_calls": tool_calls}
        logger.info(f"messages to openai: {messages}")
        completion = self.client.chat.completions.create(model=self.model, messages=messages, **kwargs)
        content = completion.choices[0].message.content
        logger.info(f"llm reply: {content}")
        return {"content": content, "finish_reason": completion.choices[0].finish_reason}

    def stream_chat(
            self,
            messages: List[Dict[str, Any]],
            tools: Optional[List[Dict[str, Any]]] = None,
            *args,
            **kwargs
    ) -> Generator:
        """
        This method streams a chat response while considering available tools and handling potential errors.

        :param messages: A list of message dictionaries for the chat conversation.
        :param tools: Optional list of available tools to use during the conversation.
        :param args: Additional positional arguments passed to the method.
        :param kwargs: Additional keyword arguments passed to the OpenAI API or other related functions.
        :return: A generator yielding partial responses or an error message.
        """
        try:
            sys_prompt = [{"role": "system", "content": SYSTEM_PROMPT}]
            msgs = sys_prompt + messages
            yield from self._get_stream_response(messages=msgs, tools=tools, **kwargs)
        except Exception as e:
            logger.error(traceback.format_exc())
            yield {"content": "Something went wrong, please try again later.", "finish_reason": "stop"}

    def chat(
            self,
            messages: List[Dict[str, Any]],
            tools: Optional[List[Dict[str, Any]]] = None,
            *args,
            **kwargs
    ) -> Dict[str, Optional[str]]:
        try:
            sys_prompt = [{"role": "system", "content": SYSTEM_PROMPT}]
            msgs = sys_prompt + messages
            return self._get_response(messages=msgs, tools=tools, **kwargs)
        except Exception as e:
            logger.error(traceback.format_exc())
            return {"content": "Something went wrong, please try again later.", "finish_reason": "stop"}


if __name__ == "__main__":
    prompt = "我有高血压怎么办"
    vision_prompt = "图中这道菜有哪些食材啊"
    from client_initializer import agent_client

    vision_msg = [{'role': 'user', 'content': [
        {'type': 'text', 'text': vision_prompt},
        {'type': 'image_url', 'image_url': {
            'url': 'https://glass-ai-test.oss-cn-shanghai.aliyuncs.com//fool.jpeg'}}]}]

    msg = [{'role': 'user', 'content': prompt}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "take_a_photo",
                "description": "Take a photo, used when visual information is needed",
                "parameters": {}
            }
        }
    ]
    # stream = input(f"stream if 1，else non-stream")
    stream = input("1 if stream else non-stream")

    if stream == "1":
        # stream
        res = agent_client.stream_chat(messages=msg, tools=tools)
        for chunk in res:
            print(chunk)


        print('\n\n vision request')
        vision_res = agent_client.stream_chat(messages=vision_msg, tools=tools)
        for chunk in vision_res:
            print(chunk)
    else:
        # non-stream
        res = agent_client.chat(messages=msg, tools=tools)
        print(f"non-stream result：{res}")

        print('\n\n vision request')
        vision_res = agent_client.chat(messages=vision_msg, tools=tools)
        print(vision_res)