from flask import Blueprint, jsonify, request
from server.services.ai_service import AIService

bp = Blueprint('ai', __name__, url_prefix='/api/ai')

@bp.route('/generate', methods=['POST'])
def generate_ai_output():
    try:
        data = request.json
        user_question = data.get('input')
        if not user_question:
            return jsonify({"error": "No input provided"}), 400
        
        answer = AIService.generate_output(user_question)
        if answer is None:
            return jsonify({"error": "Failed to generate output"}), 500
        
        return jsonify({"output": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/add-documents', methods=['POST'])
def add_documents():
    try:
        data = request.json
        raw_text = data.get('text')
        if not raw_text:
            return jsonify({"error": "No text provided"}), 400
        
        success = AIService.add_documents(raw_text)
        if not success:
            return jsonify({"error": "Failed to add documents"}), 500
        
        return jsonify({"message": "Documents added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500