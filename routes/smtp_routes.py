from flask import Blueprint, jsonify, request
from server.services.smtp_service import SMTPService

bp = Blueprint('smtp', __name__, url_prefix='/api/smtp')

@bp.route('/send', methods=['POST'])
def send_email():
    """
    This endpoint sends an email using the SMTP service.
    
    The endpoint expects a JSON payload with 'to', 'subject', and 'body' fields.
    It uses the SMTPService to send the email and returns a JSON response indicating success or failure.
    
    Example usage:
    POST /api/smtp/send
    {
        "to": "recipient@example.com",
        "subject": "Test Email",
        "body": "This is a test email sent from the SMTP route."
    }
    
    Returns:
    A JSON object with a 'success' field indicating whether the email was sent successfully.
    If an error occurs, it returns a JSON object with 'success' set to false and an 'error' field containing the error message.
    """
    data = request.json
    try:
        result = SMTPService.send_email(data['to'], data['subject'], data['body'])
        return jsonify({"success": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500