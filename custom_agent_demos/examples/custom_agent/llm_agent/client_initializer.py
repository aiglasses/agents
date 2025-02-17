# -*- encoding: utf-8 -*-
import os
from llm_agent import BaseLlmExpert


LLM_EXPERT_MAP = {
    "<qwen>": BaseLlmExpert("<qwen>"),
    "<doubao>": BaseLlmExpert("<doubao>"),
    "<deepseek>": BaseLlmExpert("<deepseek>")
}
