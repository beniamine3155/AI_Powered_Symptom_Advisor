from src.components .pdf_loader import load_pdf_file, create_text_chunks
from src.components.vector_store import save_vector_store

from src.common.custom_exception import CustomException
from src.common.logger import get_logger

logger = get_logger(__name__)

def process_and_store_pdfs():
    try:
        # Load PDF files
        logger.info("Starting PDF loading process")
        documents = load_pdf_file()
        if not documents:
            raise CustomException("No documents found")
        logger.info(f"Loaded {len(documents)} documents")

        # Create text chunks
        text_chunks = create_text_chunks(documents)
        if not text_chunks:
            raise CustomException("No text chunks created")
        logger.info(f"Created {len(text_chunks)} text chunks")

        # Save to vector store
        save_vector_store(text_chunks)
        logger.info("Successfully saved text chunks to vector store")

    except Exception as e:
        error_message = CustomException("Failed to process and store PDFs", e)
        logger.error(str(error_message))
        return error_message
    

if __name__ == "__main__":
    process_and_store_pdfs()

