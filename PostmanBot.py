from MailProcessor import MailProcessor as mail
from BaseBot import Bot
import smtplib

class PostmanBot(Bot):
    def __init__(self):
        Bot.__init__(self)
        self.last_update = ""
        self.last_chat_id= ""
        self.curr_message_id = -1
        self.last_message_id = -1
        self.mail = None
        self.start_command_recived = False
        self.default_mail_port_number = 587
    def get_service(self,login):
        mail_ch = login.index('@')
        if mail_ch == -1:
            return ''
        
        return login[mail_ch+1:]

    def send(self,command):
        pass
    def update(self):
        self.last_update = self.get_last_update()

        if "message" in  self.last_update.keys() and not self.start_command_recived:
            if self.last_update['message']['text'] == "/begin":
                self.start_command_recived = True

        if "message" in self.last_update.keys() and self.start_command_recived:
            self.last_chat_id = self.last_update['message']['chat']['id']
            self.curr_message_id= self.last_update['message']['message_id']
            text = self.last_update['message']['text']

            not_repeat = self.last_message_id != self.curr_message_id
            if "/login" in text and not_repeat:
                args = text.split(' ')
                if len(args) == 3:
                    login = args[1]
                    password = args[2]
                    service = self.get_service(login)
                    if service == '':
                       self.send_message(self.last_chat_id,"incorrect e-mail!")
                       self.last_message_id = self.curr_message_id
                    else:
                        print(f"smtp.{service}")
                        try:
                            self.mail = mail(f"smtp.{service}",self.default_mail_port_number,login,password)
                            self.send_message(self.last_chat_id,"successful login!")
                        except smtplib.SMTPAuthenticationError:
                            self.send_message(self.last_chat_id,"can not login!")
                        self.last_message_id = self.curr_message_id
                else:
                    self.send_message(self.last_chat_id,"not enough data to login!")
                    self.last_message_id = self.curr_message_id

            
            if "/quit" in text and not_repeat:
                self.last_message_id = self.curr_message_id
                self.mail = None

            send_command = "/send" in text
            if  send_command and self.mail != None and not_repeat:
                text_begin = text.find('"')
                text_end   = text.rfind('"')
                if text_begin != -1 and text_end != -1:
                    message = text[text_begin+1:text_end]
                    getters = text[text_end+1:].split(' ')
                    getters = list(filter(lambda n:len(n) > 0,getters))
                    self.mail.send(message,getters)
                    self.send_message(self.last_chat_id,"messeges are sent!")
                else:
                    self.send_message(self.last_chat_id,"incorrect input!")
                self.last_message_id = self.curr_message_id
            elif send_command and self.mail == None and not_repeat:
                self.send_message(self.last_chat_id,"you haven't login yet to send mail!")
                self.last_message_id = self.curr_message_id

bot = PostmanBot()

def main():
    while True:
        bot.update()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(-1)




