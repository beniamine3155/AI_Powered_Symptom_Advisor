from src.common.custom_exception import CustomException
from src.common.logger import get_logger

from src.components.llm import get_llm_model
from src.components.vector_store import load_vector_store
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

logger = get_logger(__name__)


CUSTOM_PROMPT_TEMPLATE = """You are an AI-Powered Symptom Advisor designed to provide medical guidance based on reliable medical information.

**Important Guidelines:**
- Only provide advice based on the medical context provided below
- Keep responses concise (3-5 lines maximum)
- If symptoms suggest serious conditions, recommend consulting a healthcare professional immediately
- Do not provide definitive diagnoses - offer guidance and suggestions only
- If the context doesn't contain relevant information, state that clearly

**Medical Context:**
{context}

**Patient Query/Symptoms:**
{question}

**Medical Guidance:**
Based on the provided medical information, """


def set_custom_prompt():
    return PromptTemplate(
        input_variables=["context", "question"],
        template=CUSTOM_PROMPT_TEMPLATE
    )


def validate_medical_query():
    try:
        logger.info("Loadin vector store for query validation")

        db = load_vector_store()
        
        if db is None:
            raise CustomException("Vector store could not be loaded for query validation")
        llm = get_llm_model()
        if llm is None:
            raise CustomException("LLM model could not be initialized for query validation")
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(search_type="similarity", search_kwargs={"k": 1}),
            return_source_documents=False,
            chain_type_kwargs={"prompt": set_custom_prompt()}
         )
        
        logger.info("Query validation chain initialized successfully")
        return qa_chain
    
    except Exception as e:
        error_message = CustomException("Failed to initialize query validation chain", e)
        logger.error(str(error_message))
        return None
    