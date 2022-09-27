from api.mail import SendMailManager


class SendEmployeeData(SendMailManager):
    def send_employee_data(self, user_data: dict):
        name = user_data.get("name", "Ошибка!")
        password = user_data.get("password", "Ошибка!")
    
        title = f"Данные пользователя {name}"
        body = f"Пароль: {password}"
        super().send(title=title, body=body)
