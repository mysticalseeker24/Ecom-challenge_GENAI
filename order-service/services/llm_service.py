from langchain_openai import ChatOpenAI

class LLMService:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,  # Lower temperature for more deterministic responses
        )

    def get_llm(self):
        return self.llm
    
