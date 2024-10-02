from langchain_anthropic import ChatAnthropic
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI

"""Place to define & configure your LLM models"""

# Anthropic Models
model_claude_3_haiku = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0)
model_claude_3_5_sonnet = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)
# Google Gemini Models - Warning: Found it low performing with both Langchain and function calling
model_gemini_1_5_flash = GoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
model_gemini_1_5_pro = GoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
# OpenAI Models
# model_gpt_3_5_turbo_0125 = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
# model_chatgpt_4o = ChatOpenAI(model="chatgpt-4o-latest", temperature=0)

# You can also define other models from other providers like Ollama, Cohere. Just make sure they use langchain library
