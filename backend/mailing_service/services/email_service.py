"""служба рассыдки почтовых сообщений"""#pylint: disable=E0401, W0718
import resend
from mailing_service.schemas.message import EmailData
from shared.config.base import settings


class EmailService:
    """класс службы"""
    def __init__(self):
        resend.api_key = settings.RESEND_API_KEY
        self.default_from = settings.RESEND_FROM_EMAIL

    async def send_email(self, email_data: EmailData) -> bool:
        """Асинхронная отправка email через Resend"""
        try:
            params = {
                "from": email_data.from_email or self.default_from,
                "to": email_data.to,
                "subject": email_data.subject,
                "html": email_data.html,
            }

            response = resend.Emails.send(params)
            print(f"Email sent successfully: {response}")
            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    async def send_welcome_email(self, to_email: str, username: str) -> bool:
        """Отправка приветственного письма"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4F46E5;">Добро пожаловать в CFDChamp, {username}!</h2>
                <p>Спасибо за регистрацию в нашем сервисе.</p>
            </div>
        </body>
        </html>
        """

        email_data = EmailData(
            to=[to_email],
            subject="Добро пожаловать в CFDChamp!",
            html=html_content
        )

        return await self.send_email(email_data)

email_service = EmailService()

class EmailServiceSync:
    """Синхронный класс службы для Celery"""
    def __init__(self):
        resend.api_key = settings.RESEND_API_KEY
        self.default_from = settings.RESEND_FROM_EMAIL

    def send_email(self, email_data: EmailData) -> bool:
        """Синхронная отправка email через Resend"""
        try:
            params = {
                "from": email_data.from_email or self.default_from,
                "to": email_data.to,
                "subject": email_data.subject,
                "html": email_data.html,
            }

            response = resend.Emails.send(params)
            print(f"Email sent successfully: {response}")
            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

email_service_sync = EmailServiceSync()
