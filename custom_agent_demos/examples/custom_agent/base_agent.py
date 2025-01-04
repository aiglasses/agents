# -*- encoding: utf-8 -*-

from typing import Optional


class BaseAgent(object):
    def __init__(self):
        self._agent_name = self.__class__.__name__

    def stream_chat(self, *args, **kwargs):
        raise NotImplemented("subclass must implement the stream_chat method.")

    def chat(self, *args, **kwargs):
        raise NotImplemented("subclass must implement the chat method.")