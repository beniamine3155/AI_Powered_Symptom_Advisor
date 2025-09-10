from langchain_openai import ChatOpenAI
from src.config.config import OPENAI_API_KEY

from src.common.custom_exception import CustomException
from src.common.logger import get_logger


logger = get_logger(__name__)

def get_llm_model():
    try:
        if not OPENAI_API_KEY:
            raise CustomException("OpenAI API key is not set in environment variables.")
        
        logger.info("Initializing ChatOpenAI model")
        llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0,
            openai_api_key=OPENAI_API_KEY
        )
        
        return llm
    
    except Exception as e:
        error_message = CustomException("Failed to initialize LLM model",e)
        logger.error(str(error_message))
        return None