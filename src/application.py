from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.components.retriever import validate_medical_query, set_custom_prompt
from src.common.custom_exception import CustomException
from src.common.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Global QA chain instance
qa_chain = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global qa_chain
    try:
        logger.info("Initializing AI Symptom Advisor...")
        qa_chain = validate_medical_query()
        if qa_chain:
            logger.info("AI Symptom Advisor initialized successfully")
        else:
            logger.error("Failed to initialize AI Symptom Advisor")
    except Exception as e:
        logger.error(f"Startup error: {e}")
    
    yield  # Application runs here
    
    # Cleanup (if needed)
    logger.info("Shutting down AI Symptom Advisor...")

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Symptom Advisor",
    description="An intelligent medical advisory system powered by AI",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Pydantic models for request/response
class ChatMessage(BaseModel):
    message: str
    timestamp: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    confidence: str
    timestamp: str
    disclaimer: str
    success: bool = True

class ChatHistory(BaseModel):
    messages: List[dict]

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    try:
        html_file = Path(__file__).parent / "static" / "index.html"
        if html_file.exists():
            with open(html_file, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        else:
            return HTMLResponse(
                content="<h1>Welcome to AI-Powered Symptom Advisor</h1><p>Please create index.html in static folder</p>"
            )
    except Exception as e:
        logger.error(f"Error serving HTML: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    """Handle chat messages and return medical advice"""
    global qa_chain
    
    try:
        if not message.message or len(message.message.strip()) < 3:
            return ChatResponse(
                response="Please provide a more detailed description of your symptoms or medical question.",
                confidence="low",
                timestamp="",
                disclaimer="",
                success=False
            )
        
        logger.info(f"Processing chat message: {message.message}")
        
        # Check if QA chain is initialized
        if not qa_chain:
            logger.warning("QA chain not initialized, attempting to reinitialize...")
            qa_chain = validate_medical_query()
            
        if not qa_chain:
            return ChatResponse(
                response="I'm currently unable to process your request. Please try again later or consult a healthcare professional.",
                confidence="low",
                timestamp="",
                disclaimer="",
                success=False
            )
        
        # Process the query
        result = qa_chain({"query": message.message})
        
        # Extract response
        advice = result.get("result", "I'm unable to provide specific advice for your query.")
        
        # Add emergency detection
        emergency_keywords = ["chest pain", "difficulty breathing", "severe bleeding", "unconscious"]
        is_emergency = any(keyword in message.message.lower() for keyword in emergency_keywords)
        
        if is_emergency:
            advice = "🚨 EMERGENCY: Your symptoms may require immediate medical attention. Please call emergency services or visit the nearest emergency room immediately. " + advice
            confidence = "high"
        else:
            confidence = "medium"
        
        # Medical disclaimer
        disclaimer = "⚠️ This advice is for informational purposes only and should not replace professional medical consultation. Please consult a healthcare provider for proper diagnosis and treatment."
        
        response = ChatResponse(
            response=advice,
            confidence=confidence,
            timestamp=message.timestamp or "",
            disclaimer=disclaimer,
            success=True
        )
        
        logger.info("Chat response generated successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return ChatResponse(
            response="I encountered an error processing your request. Please try again or consult a healthcare professional.",
            confidence="low",
            timestamp="",
            disclaimer="",
            success=False
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global qa_chain
    
    status = "healthy" if qa_chain else "unhealthy"
    return {
        "status": status,
        "qa_chain_initialized": qa_chain is not None,
        "message": "AI Symptom Advisor is running"
    }

@app.post("/reset-session")
async def reset_session():
    """Reset the chat session"""
    try:
        logger.info("Chat session reset requested")
        return {"message": "Session reset successfully", "success": True}
    except Exception as e:
        logger.error(f"Error resetting session: {e}")
        raise HTTPException(status_code=500, detail="Failed to reset session")

@app.get("/api/info")
async def get_app_info():
    """Get application information"""
    return {
        "app_name": "AI-Powered Symptom Advisor",
        "version": "1.0.0",
        "description": "An intelligent medical advisory system",
        "features": [
            "Medical symptom analysis",
            "AI-powered advice generation",
            "Emergency situation detection",
            "Medical knowledge base integration"
        ]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    host = os.getenv("HOST", "127.0.0.1")
    
    logger.info(f"Starting AI-Powered Symptom Advisor on {host}:{port}")
    
    uvicorn.run(
        "application:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
