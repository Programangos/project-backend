import resend
from django.conf import settings


class EmailService:
    def __init__(self):
        resend.api_key = settings.RESEND_API_KEY

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
        params = {
            "from": settings.RESEND_FROM_EMAIL,
            "to": [to_email],
            "subject": "Recuperación de contraseña - SISA",
            "html": html,
        }
        resend.Emails.send(params)
