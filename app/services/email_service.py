# email_service.py
from builtins import ValueError, dict, str
from settings.config import settings
from app.utils.smtp_connection import SMTPClient
from app.utils.template_manager import TemplateManager
from app.models.user_model import User
from app.utils.translation import translate  # Import the translate function
import logging

class EmailService:
    def __init__(self, template_manager: TemplateManager):
        self.smtp_client = SMTPClient(
            server=settings.smtp_server,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password
        )
        self.template_manager = template_manager

    async def send_user_email(self, user_data: dict, email_type: str):
        subject_map = {
            'email_verification': "Verify Your Account",
            'password_reset': "Password Reset Instructions",
            'account_locked': "Account Locked Notification"
        }

        if email_type not in subject_map:
            raise ValueError("Invalid email type")

        html_content = self.template_manager.render_template(email_type, **user_data)
        self.smtp_client.send_email(subject_map[email_type], html_content, user_data['email'])

    async def send_verification_email(self, user: User):
        # Determine user's preferred language; default to 'en' if not provided
        lang = user.preferred_language if user.preferred_language else "en"

        # Translate email subject and content
        email_subject = translate(lang, "email_verification_subject")
        email_content = translate(lang, "email_verification_content")

        verification_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"
        html_content = self.template_manager.render_template(
            "email_verification",
            name=user.first_name or user.nickname,  # Fallback to nickname if first_name is None
            verification_url=verification_url,
            email_content=email_content  # Inject translated content
    )

        # Send email - assumed synchronous
        if settings.send_real_mail:
            self.smtp_client.send_email(email_subject, html_content, user.email)
        else:
            logging.info("Email sending is disabled. Skipping email.")
