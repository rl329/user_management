# email_service.py
from builtins import ValueError, dict, str
from settings.config import settings
from app.utils.smtp_connection import SMTPClient
from app.utils.template_manager import TemplateManager
from app.models.user_model import User
from app.utils.translation import translate  # Import the translate function
from urllib.parse import urljoin  # Safely concatenate URLs
import logging

class EmailService:
    def __init__(self, template_manager: TemplateManager):
        """
        Initialize the EmailService with SMTP client and template manager.
        """
        self.smtp_client = SMTPClient(
            server=settings.smtp_server,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password
        )
        self.template_manager = template_manager

    async def send_user_email(self, user_data: dict, email_type: str):
        """
        Send a general user email based on a specific email type.

        Args:
            user_data (dict): User data to populate the template.
            email_type (str): Type of email (e.g., email_verification, password_reset).
        """
        subject_map = {
            'email_verification': "Verify Your Account",
            'password_reset': "Password Reset Instructions",
            'account_locked': "Account Locked Notification"
        }

        if email_type not in subject_map:
            raise ValueError("Invalid email type")

        # Render the email content using the template
        html_content = self.template_manager.render_template(email_type, **user_data)

        # Send the email
        self.smtp_client.send_email(subject_map[email_type], html_content, user_data['email'])

    async def send_verification_email(self, user: User):
        """
        Send an email verification link to the user.

        Args:
            user (User): User model containing user details.
        """
        # Determine the user's preferred language, default to English
        lang = user.preferred_language if user.preferred_language else "en"

        # Translate email subject and content
        email_subject = translate(lang, "email_verification_subject")
        email_greeting = translate(lang, "hello").format(name=user.first_name or user.nickname)
        email_content = translate(lang, "email_verification_content")
        email_cta = translate(lang, "button_verify_email")
        email_thanks = translate(lang, "footer_thanks")
        email_footer = translate(lang, "footer_unsubscribe").format(
            here="<a href='unsubscribe_link'>here</a>"
        )

        # Safely construct the verification URL
        verification_url = urljoin(
            str(settings.server_base_url),
            f"verify-email/{user.id}/{user.verification_token}"
        )

        # Debug logging to verify variable values
        logging.debug(f"Base URL: {settings.server_base_url}")
        logging.debug(f"Verification URL: {verification_url}")

        # Combine all parts of the email into a single HTML body
        html_content = f"""
            <html>
                <body>
                    <p>{email_greeting}</p>
                    <p>{email_content}</p>
                    <p><a href="{verification_url}">{email_cta}</a></p>
                    <p>{email_thanks}</p>
                    <hr>
                    <p style="font-size:small;">{email_footer}</p>
                </body>
            </html>
        """

        # Send the email
        if settings.send_real_mail:
            self.smtp_client.send_email(email_subject, html_content, user.email)
        else:
            logging.info("Email sending is disabled. Skipping email.")
