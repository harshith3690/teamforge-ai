
import os
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL", "qwen2.5:3b")
OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)
MAX_REVISIONS = int(os.getenv("MAX_REVISIONS", "2"))
