import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

FROM_EMAIL = os.environ.get('FROM_EMAIL')
FROM_PWD = os.environ.get('FROM_PWD')

#TODO: handle errors if no internet or wrong password

def send_email_from_gmail(assistant):
    assistant.talk('who would you like to send the email to?')
    to_email = input('To: ')
    
    assistant.talk('what would the subject be?')
    subject = input("Subject for the E-mail(recommended): ")
    
    assistant.talk('what would the message be?')
    msg = input("Message: ")

    #prepare the message
    message = MIMEMultipart()
    message['From'] = FROM_EMAIL
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(msg, 'plain'))

    #send the message
    assistant.session.starttls()
    assistant.session.login(FROM_EMAIL, FROM_PWD)
    text = message.as_string() 
    assistant.session.sendmail(FROM_EMAIL, to_email, text)
    assistant.session.quit()

    assistant.talk(f'your email has been send to {to_email}')