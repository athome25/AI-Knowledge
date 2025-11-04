import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv


load_dotenv()

model_name = os.getenv("MODEL_NAME")
base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")

llm = ChatAnthropic(model=model_name, base_url=base_url, api_key=api_key)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Who won the 2000 Australian Open?")
]

response = llm.invoke(messages)

print("Response:", response.content)
