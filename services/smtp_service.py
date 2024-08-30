import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SMTPService:
    @staticmethod
    def send_email(to, subject, body):
        # Your Outlook email credentials
        from_email = "your_outlook_email@outlook.com"
        password = "your_outlook_password"

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to
        msg['Subject'] = subject

        # Add body to email
        msg.attach(MIMEText(body, 'plain'))

        # Outlook SMTP server settings
        smtp_server = "smtp.office365.com"
        port = 587  # For starttls

        try:
            # Create a secure SSL context
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()  # Secure the connection

            # Login to the server
            server.login(from_email, password)

            # Send email
            server.send_message(msg)
            print("Email sent successfully!")
            return True

        except Exception as e:
            print(f"An error occurred: {e}")
            return False

        finally:
            server.quit()
