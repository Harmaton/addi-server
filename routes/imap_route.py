from flask import Blueprint, jsonify, request
from services.imap_service import IMAPService

bp = Blueprint('imap', __name__, url_prefix='/api/imap')

@bp.route('/fetch', methods=['POST'])
def fetch_emails():
    try:
        data = request.json
        email_address = data['username']
        password = data['password']
        num_emails = data.get('num_emails', 3)

        emails = IMAPService.fetch_emails(email_address, password, num_emails)
        return jsonify(emails)
    except Exception as e:
        return jsonify({"error": str(e)}), 500