from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os
from pathlib import Path

# Fix OpenMP issue
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.components.retriever import validate_medical_query

from dotenv import load_dotenv
load_dotenv()

def create_app():
    
    app = Flask(__name__)
    CORS(app)
    
    # Initialize QA chain
    qa_chain = validate_medical_query()
    
    @app.route("/")
    def index():
        html_file = Path(__file__).parent / "static" / "index.html"
        if html_file.exists():
            with open(html_file, "r", encoding="utf-8") as f:
                return f.read()
        return "<h1>AI-Powered Symptom Advisor</h1>"
    
    @app.route("/chat", methods=["POST"])
    def get_response():
        data = request.get_json()
        user_input = data.get("message", "")
        
        if not qa_chain:
            return jsonify({"response": "Service unavailable", "success": False})
        
        result = qa_chain.invoke({"query": user_input})
        advice = result.get("result", "I'm unable to provide advice.")
        
        # Emergency detection
        emergency_keywords = ["chest pain", "difficulty breathing", "severe bleeding", "unconscious"]
        if any(keyword in user_input.lower() for keyword in emergency_keywords):
            advice = "EMERGENCY: Seek immediate medical attention! " + advice
        
        disclaimer = "This is for informational purposes only. Consult a healthcare provider."
        
        return jsonify({
            "response": advice,
            "disclaimer": disclaimer,
            "success": True
        })
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8001, debug=True)
