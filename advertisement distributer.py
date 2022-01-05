import smtplib
from email.mime.text import MIMEText
import time
import random

# Python script that obtains a URL from the user and finds all emails on the provided webpage and saves them to a text file.
# The program then sends emails to the created list with a specified marketing message via SMTP (Simple Mail Transfer Protocol).


#it use to take urls and scrape from urls but it was buggy so I made it read from the file. but here is what the code looks like:
#from: https://www.thepythoncode.com/article/extracting-email-addresses-from-web-pages-using-python

# import re
# from requests_html import HTMLSession
# try:
#     url = input("enter a url: ")
#     Identifys if email or not
#     email_identifer = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
#     starts the HTMLSession
#     session = HTMLSession()
#     r = session.get(url)
#     only for javascript websites
#     r.html.render()
#     for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
#         writes all the found emails to the email file
#         emailFile.writelines(re_match.group())
# except Exception as e:
#     print(e)
#     exit(0)




#input for email
email = input("email: ")
#input for password
password = input("password: ")

#asks for the file to get the emails from
fileName =input("enter the file name: ")
emailFile = open(fileName, 'r')
fileContents = emailFile.readlines()
recipients = []


try:
    #strip the end line off of each line of the file
    newFileContent= map(lambda s: s.strip(), fileContents)
    for email in range(len(fileContents)):
        #generate a random value from 60 to 150
        timer = random.randrange(60,150)
        recipients.append(fileContents[email])
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.starttls()
        mail.ehlo()
        mail.login(email, password)
        mail.set_debuglevel(1)
        msg = MIMEText("""Hello Viewer, This is the Founder of The Rikers Times. The Rikers Times is a new way of consuming media in a state of the art way, with a comedic twist. Our writers spend countless hours writing these articles and making sure that they are the most accurate for your viewing pleasure. We at Rikers want to revolutionize the way that people read news. Check out our website at: https://therikerstimes.wixsite.com/mysite. Be sure to subscribe to our free weekly newsletter as every subscription helps us immensely. If you like our content, please don't hesitate to share with you friends.
        Thank you in advance,
        The Rikers Times""")
        msg['Subject'] = "BREAKING NEWS - THE RIKERS TIMES"
        msg['Bcc'] =", ".join(recipients)
        mail.sendmail(email, recipients, msg.as_string())
        #send the email if there are three people in the recipients list
        if len(recipients)%3==0:
            print("sending to: %s" % recipients)
            print("sleeping for %r seconds" % timer)
            recipients.clear()
            #sleep for the value of timer
            time.sleep(timer)
        #print the last three people in the file (gmail has a limit to how many people you can send to at once.)
        elif(len(fileContents)-email<3):
            print("sending to: %s" % recipients)
            recipients.clear()

except Exception as e:
    print(str(e))