import smtplib as _mail


class MailProcessor:
    def __init__(self,service,service_port_number, login,password):
        self.mail = _mail.SMTP(service,service_port_number)
        self.mail.starttls()
        self.mail.login(login,password)
        self.login = login

    def send(self,message, getters):
        self.mail.sendmail(self.login,getters,message)