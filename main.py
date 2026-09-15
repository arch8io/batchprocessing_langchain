import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Point to OpenRouter using a completely free model
llm = ChatOpenAI(
    # Option 1: Meta Llama 3.3 70B Free
    # model="meta-llama/llama-3.3-70b-instruct:free",
    
    # Option 2: Google Gemini Flash 2.0 Free (Alternative)
    # model="google/gemini-2.0-flash-exp:free",
    
    model="nvidia/nemotron-3-ultra-550b-a55b:free",

    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0,
)

prompt = """You need to classify the reason for the user's feedback.
The categories include: too expensive, insufficient after-sales support, poor product quality, others.
The response format is: Classification result: xx.
The user's issue is: The cost-performance ratio is not high, I don't think it's worth the money.
"""

result = llm.invoke(prompt)
print(result.content)
