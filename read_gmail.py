import email

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------

#TODO: handle errors if no internet or wrong password
#TODO: maximum number of unseen emails to read

def read_email_from_gmail(assistant):
    '''
        handle the unseend emails from google ('read') 
    '''
    _type, data = assistant.mail.search(None, '(UNSEEN)')
    id_list = data[0].split()
    
    if id_list:
        if len(id_list) > 1:
            assistant.talk(f'you have {len(id_list)} new emails, would you like me to read the headlines?')
        else:
            assistant.talk(f'you have {len(id_list)} new email, would you like me to read the headlines?')
        
        decision = input('yes/no? ')

        if decision == 'yes':        
            for (n, num) in enumerate(id_list):
                typ, data = assistant.mail.fetch(num, '(RFC822)')
                
                raw_data = data[0][1].decode('utf-8') # you could get message_from_bytes otherwise
                
                msg = email.message_from_string(raw_data)
                
                email_subject = msg['subject']
                email_from = msg['From']
                
                if "<" in email_from:
                    from_name, from_email = email_from.split('<')
                    from_email = from_email[0:-1].strip()
                    from_name = from_name.strip() #get rid of space
                    
                    assistant.talk(f'email number {str(n + 1)}, from {from_name}, with the subject, ({email_subject})')
                
                    print('From: '+from_email, from_name, 'Subject: ', email_subject)
                
                else:
                    assistant.talk(f'email number {str(n + 1)}, from {email_from}, with the subject, ({email_subject})')
                    print('From: '+email_from, 'Subject: ', email_subject)
        
        else: #decision
            assistant.talk("okay, do you need anything else?")
    
    else:
        assistant.talk("you don't have any new emails")  
