from api.mail import SendMailManager


class SendEmployeePassword(SendMailManager):
    def send_password(self, password):
        title = "Регистрация на платформе TT-Crm"
        body = f"Ваш пароль: {password}\nНастоятельно рекомендуем сменить временный пароль в профиле"
        super().send(title=title, body=body)
