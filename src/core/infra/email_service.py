from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To
from django.conf import settings


class EmailService:
    def __init__(self):
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)

    def send_password_reset(self, to_email: str, token: str, frontend_url: str | None = None):
        base_url = frontend_url or settings.FRONTEND_URL
        reset_link = f"{base_url}/reset-password?token={token}"
        html = f"""
        <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto;">
            <h2 style="color: #1e293b;">Recuperación de contraseña - SISA</h2>
            <p style="color: #475569;">Haz clic en el siguiente enlace para restablecer tu contraseña. Este enlace expira en 1 hora.</p>
            <a href="{reset_link}"
               style="display: inline-block; background-color: #4338ca; color: white; padding: 12px 24px;
                      text-decoration: none; font-weight: bold; border-radius: 4px; margin: 16px 0;">
                Restablecer contraseña
            </a>
            <p style="color: #94a3b8; font-size: 12px;">Si no solicitaste este cambio, ignora este correo.</p>
        </div>
        """
        message = Mail(
            from_email=From(settings.SENDGRID_FROM_EMAIL),
            to_emails=To(to_email),
            subject="Recuperación de contraseña - SISA",
            html_content=html,
        )
        self.client.send(message)
