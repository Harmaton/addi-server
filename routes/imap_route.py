from flask import Blueprint, jsonify, request
from services.imap_service import IMAPService

bp = Blueprint('imap', __name__, url_prefix='/api/imap')

@bp.route('/fetch', methods=['POST'])
def fetch_emails():
    """
    This endpoint fetches emails from an outlook IMAP server.
    
    The endpoint uses the IMAPService to fetch the emails and returns them as a JSON response.
    
    Example usage:
    POST /api/imap/fetch
    {
        "username": "user@example.com",
        "password": "password123",
        "num_emails": 5
    }
    
    Returns:
    A JSON array of email objects, each containing details like subject, sender, date, body, and attachments.
    If an error occurs, it returns a JSON object with an 'error' field containing the error message.
    """
    try:
        data = request.json
        email_address = data['username']
        password = data['password']
        num_emails = data.get('num_emails', 3)

        emails = IMAPService.fetch_emails(email_address, password, num_emails)
        return jsonify(emails)
    except Exception as e:
        return jsonify({"error": str(e)}), 500