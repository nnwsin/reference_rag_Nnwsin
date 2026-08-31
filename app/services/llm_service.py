from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0,
    )