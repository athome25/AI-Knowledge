import os
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

model_name = os.getenv("MODEL_NAME")
base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")

llm = ChatAnthropic(model=model_name, base_url=base_url, api_key=api_key)