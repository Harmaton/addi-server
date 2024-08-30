import imaplib
import email
from email.header import decode_header
from google.cloud import storage
import uuid

IMAP_SERVER = 'outlook.office365.com'
import os
from dotenv import load_dotenv

load_dotenv()
BUCKET_NAME = os.getenv('BUCKET_NAME')
PROJECT_ID=os.getenv('PROJECT_ID')

class IMAPService:
    @staticmethod
    def fetch_emails(email_address, password, num_emails=3):
        # Connect to the Outlook IMAP server
        imap_conn = imaplib.IMAP4_SSL(IMAP_SERVER)

        try:
            # Login to the email account
            imap_conn.login(email_address, password)

            # Select the inbox
            imap_conn.select('INBOX')

            # Search for all emails and get the latest ones
            _, message_numbers = imap_conn.search(None, 'ALL')
            latest_emails = message_numbers[0].split()[-num_emails:]

            emails = []
            for num in reversed(latest_emails):
                _, msg_data = imap_conn.fetch(num, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        email_body = response_part[1]
                        email_message = email.message_from_bytes(email_body)
                        
                        # Decode the subject properly
                        subject = ""
                        subject_parts = decode_header(email_message['Subject'])
                        for content, encoding in subject_parts:
                            if isinstance(content, bytes):
                                subject += content.decode(encoding or 'utf-8')
                            else:
                                subject += content
                        
                        sender = email_message['From']
                        
                        # Get email content
                        body = ""
                        attachments = []
                        
                        if email_message.is_multipart():
                            for part in email_message.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    body = part.get_payload(decode=True).decode()
                                elif "attachment" in content_disposition:
                                    filename = part.get_filename()
                                    if filename:
                                        # Generate a unique filename
                                        unique_filename = f"{uuid.uuid4()}_{filename}"
                                        
                                        # Upload attachment to Google Cloud Storage
                                        storage_client = storage.Client()
                                        bucket = storage_client.bucket(BUCKET_NAME)
                                        blob = bucket.blob(f"{sender}/{unique_filename}")
                                        blob.upload_from_string(
                                            part.get_payload(decode=True),
                                            content_type=content_type
                                        )
                                        
                                        # Store the public URL of the uploaded file
                                        attachments.append(blob.public_url)
                        else:
                            body = email_message.get_payload(decode=True).decode()
                        
                        emails.append({
                            'subject': subject,
                            'sender': sender,
                            'date': email_message['Date'],
                            'body': body,
                            'attachments': attachments
                        })

            return emails

        except imaplib.IMAP4.error as e:
            print(f"Error connecting to Outlook: {e}")
            return []

        finally:
            # Ensure the connection is closed even if an error occurs
            if 'imap_conn' in locals():
                imap_conn.logout()

    @staticmethod
    def initialize_google_cloud_storage():
        try:
            storage.Client(project=PROJECT_ID)
            return {"message": "Google Cloud Storage initialized successfully"}
        except Exception as e:
            print(f"Error initializing Google Cloud Storage: {str(e)}")
            return None
