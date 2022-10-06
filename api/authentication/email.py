from api.mail import SendMailManager


class SendCode(SendMailManager):
    def __init__(self, to=None) -> None:
        super().__init__(to)

    def send_code(self, code):
        title = "Код смены пароля TT-Crm"
        body = f"Код: {code}"
        super().send(title=title, body=body)
