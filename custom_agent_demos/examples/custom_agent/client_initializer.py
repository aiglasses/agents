# -*- encoding: utf-8 -*-
import os
from food_agent import FoodAgent

MODEL = "qwen-plus"
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
agent_client = FoodAgent(model="qwen-plus", api_key=API_KEY, base_url=BASE_URL)
