import os
from langchain_community.vectorstores import FAISS

from src.components.embedding import get_embedding_model
from src.config.config import DB_FAISS_PATH

from src.common.custom_exception import CustomException
from src.common.logger import get_logger

logger = get_logger(__name__)

def load_vector_store():
    try:
        embedding_model = get_embedding_model()

        if os.path.exists(DB_FAISS_PATH):
            logger.info(f"Loading existing FAISS vector store from {DB_FAISS_PATH}")
            return FAISS.load_local(
                DB_FAISS_PATH, 
                embedding_model,
                allow_dangerous_deserialization=True
            )
        else:
            logger.warning(f"FAISS vector store path {DB_FAISS_PATH} does not exist.")
    
    except Exception as e:
        error_message = CustomException("Failed to load FAISS vector store",e)
        logger.error(str(error_message))
        
        
        
    
def save_vector_store(text_chunks):
    try:
        if not text_chunks:
            raise CustomException("No text chunks provided to save to vector store.")
        
        embedding_model = get_embedding_model()

        logger.info(f"Creating new FAISS vector store at {DB_FAISS_PATH}")
        db = FAISS.from_documents(text_chunks, embedding_model)

        logger.info(f"Saving FAISS vector store to {DB_FAISS_PATH}")

        db.save_local(DB_FAISS_PATH)

        logger.info("FAISS vector store saved successfully")

        return db
    
    except Exception as e:
        error_message = CustomException("Failed to save FAISS vector store",e)
        logger.error(str(error_message))
        return error_message
