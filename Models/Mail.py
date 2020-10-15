from app import app
from email.mime.text import MIMEText
import smtplib


class Mail():
    def __init__(self):
        self.username = app.config["MAIL_USERNAME"]
        self.password = app.config["MAIL_PASSWORD"]
        self.smtp = smtplib.SMTP("smtp.gmail.com:587")
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login(self.username, self.password)

    def send(self, to: list, subject: str, text: str) -> bool:
        try:
            message = MIMEText(text, 'plain', 'utf-8')
            message['Subject'] = subject
            message['From'] = self.username
            message['To'] = ','.join(to)
            self.smtp.sendmail(
                message['From'], message['To'], message.as_string())
            return True
        except:
            return False

    def send_signup_verify(self, to: str, token: str, name: str) -> bool:
        text = "{} 您好!\n歡迎註冊Ticket to Ticket，以下為驗證連結，請於一小時內點選以下連結驗證信箱，若無法驗證信箱請複製至瀏覽器開啟即可驗證。\n\n{}/signup/verify/{}".format(
            name, app.config["BASE_URL"], token)
        subject = "Ticket to Ticket 帳號註冊驗證信"
        return self.send([to], subject, text)
