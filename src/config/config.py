import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Get the project root directory (parent of src)
PROJECT_ROOT = Path(__file__).parent.parent.parent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_FAISS_PATH = str(PROJECT_ROOT / "vectorstore" / "db_faiss")
DATA_PATH = str(PROJECT_ROOT / "data") + "/"
CHUNK_SIZE=500
CHUNK_OVERLAP=50
