import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    msg=EmailMessage()
    msg.set_content(body)
    msg['subject']=subject
    msg['to']=to
    msg['from']="Roshan"

    user='@email.com'
    password='password'

    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

if __name__=='__main__':
    email_alert("test", "wow it's working", "crce.9494.ecs@gmail.com")