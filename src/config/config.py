import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_FAISS_PATH="vectorstore/db_faiss"
DATA_PATH="data/"
CHUNK_SIZE=500
CHUNK_OVERLAP=50
