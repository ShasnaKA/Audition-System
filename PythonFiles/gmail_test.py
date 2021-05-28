# Python code for Sending mail from
# your Gmail account
import smtplib

def send_mail(subject,message,to):

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    gmail_id = 'shassample@gmail.com'
    gmail_password = 'shassample@123'
    s.login(gmail_id, gmail_password)

    # message to be sent
    message = 'Subject: {}\n\n\n\n{}'.format(subject, message)

    # sending the mail
    s.sendmail(gmail_id, to, message)

    print(to, message)

    # terminating the session
    s.quit()

#send_mail("Subject-Login Details","msg-hai",'to-kites.sarath@gmail.com')