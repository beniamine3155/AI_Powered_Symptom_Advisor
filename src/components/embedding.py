from langchain_openai import OpenAIEmbeddings

from src.common.custom_exception import CustomException
from src.common.logger import get_logger


logger = get_logger(__name__)

def get_embedding_model():
    try:
        logger.info("Initializing OpenAI Embedding Model")
        embedding_model = OpenAIEmbeddings()
        logger.info("OpenAI Embedding Model initialized successfully")
        return embedding_model
    
    except Exception as e:
        error_message = CustomException("Failed to initialize embedding model", e)
        logger.error(str(error_message))
        return error_message
