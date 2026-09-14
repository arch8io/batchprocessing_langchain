import os
from dotenv import load_dotenv
from langchain_xai import ChatXAI

load_dotenv()

llm = ChatXAI(
    model="grok-beta",
    temperature=0
)

prompt = """You need to classify the reason for the user's feedback.
The categories include: too expensive, insufficient after-sales support, poor product experience, others.
The response format is: Classification result: xx.
The user's issue is: The cost-performance ratio is not high, I don't think it's worth the price."""

result = llm.invoke(prompt)
print(result.content)
