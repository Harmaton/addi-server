from flask import Blueprint, jsonify, request
from server.services.ai_service import AIService

bp = Blueprint('ai', __name__, url_prefix='/api/ai')

@bp.route('/generate', methods=['POST'])
def generate_ai_output():
    data = request.json
    output1 = AIService.generate_output1(data['input'])
    output2 = AIService.generate_output2(data['input'])
    return jsonify({"output1": output1, "output2": output2})