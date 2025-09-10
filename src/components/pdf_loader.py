import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.common.custom_exception import CustomException
from src.common.logger import get_logger
from src.config.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP


logger = get_logger(__name__)


def load_pdf_file():
    try:
        if not os.path.exists(DATA_PATH):
            raise CustomException(f"The specified path {DATA_PATH} does not exist.")
        
        logger.info(f"Loading PDF files from directory: {DATA_PATH}")
        loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)

        documents = loader.load()

        if not documents:
            logger.warning(f"No PDF files found in the directory")
        else:
            logger.info(f"Loaded {len(documents)} documents from PDF files")

    except Exception as e:
        error_message = CustomException("Failed to load pdf",e)
        logger.error(str(error_message))
        return []
    

def create_text_chunks(documents):
    try:
        if not documents:
            raise CustomException("No documents to process for text chunking.")
        
        logger.info("Starting text chunking process")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

        text_chunk = text_splitter.split_documents(documents)

        logger.info(f"Created {len(text_chunk)} text chunks from documents")

        return text_chunk
    
    except Exception as e:
        error_message = CustomException("Failed to create text chunks",e)
        logger.error(str(error_message))
        return []
