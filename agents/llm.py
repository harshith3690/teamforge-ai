
from langchain_ollama import ChatOllama
from config import MODEL, OLLAMA_BASE_URL

llm = ChatOllama(
    model=MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.2,
    num_predict=500,
)

def invoke_llm(prompt: str) -> str:
    """Generate a response using the local Ollama model."""
    response = llm.invoke(prompt)
    content = response.content

    return content if isinstance(content, str) else str(content)
