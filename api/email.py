from django.conf import settings
from django.core.mail import EmailMessage


class SendMailManager:
    def __init__(self, to=None) -> None:
        self.to = to
    
    def send(self, title="title", body="body"):
        msg = EmailMessage(
            subject=title,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=self.to
        )
        return msg.send()
