import pytest
from app.services.email_service import EmailService
from app.utils.template_manager import TemplateManager
from unittest.mock import Mock
from app.models.user_model import User  # Add this import

@pytest.mark.asyncio
async def test_send_markdown_email(email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    await email_service.send_user_email(user_data, 'email_verification')
    # Manual verification in Mailtrap

async def test_email_verification_subject(mock_smtp):
    email_service = EmailService(mock_smtp)
    user = User(nickname="john", preferred_language="es", verification_token="token123")
    # Rest of the test logic...

    async def test_email_verification_link():
        mock_smtp = Mock()
        email_service = EmailService(mock_smtp)
        user = User(id=1, preferred_language="en", verification_token="token123")
        email_service.send_verification_email(user)
        args, _ = mock_smtp.send_email.call_args
        assert f"/verify-email/{user.id}/{user.verification_token}" in args[1]  # Check body content
