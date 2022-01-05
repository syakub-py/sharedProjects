import pyttsx3
import webbrowser
from googleapiclient.discovery import build
import speech_recognition as sr
#everything needed to send emails
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from datetime import date
import requests
import subprocess
import os
import socket
import yfinance as yf
import calendar
import os.path


speak1 = ""
search1 = ""
stock1 = ""


# Performs basic tasks like telling the weather, opening and sending emails, setting alarms, and other tasks that the user wants to automate.
# It can also move files into folders, create new folders and files, and delete files for a certain folder.
# Additionally, it can monitor a set of 7-10 stocks that the user inputs, providing the open, current, and closing stock prices, daily trading volume, and any stock splits that occurred recently.
# The python script allows the user to monitor a portfolio, giving up-to-date information.
# This Python program uses a local text to speech converter called pyttsx3 that allows it to speak.
# It uses the Python speech recognition library (SpeechRecognizer) to convert the spoken commands to text.



def speechRecegnizer():
    r = sr.Recognizer()
    #set the mic as the source of audio
    with sr.Microphone() as source:
        print("listening... ")
        try:
            audio = r.listen(source)
            #convert the audio to text using google translate
            my_command1 = r.recognize_google(audio)
            print(my_command1)
        except:
            speak("I didnt catch that")
    #return the spoken command
    return my_command1

def date_time():
    hour = int(datetime.now().hour)
    min = int(datetime.now().minute)
    day = datetime.now().day
    my_date = date.today()
    weekday = calendar.day_name[my_date.weekday()]
    month = datetime.now().month
    year = datetime.now().year

    if month == 1:
        month = "january"
    if month == 2:
        month = "February"
    if month == 3:
        month = "march"
    if month == 4:
        month = "april"
    if month == 5:
        month = "may"
    if month == 6:
        month = "june"
    if month == 7:
        month = "july"
    if month == 8:
        month = "august"
    if month == 9:
        month = "september"
    if month == 10:
        month = "october"
    if month == 11:
        month = "november"
    if month == 12:
        month = "december"
    if hour >= 0 and hour < 12:
        speak("Good Morning, today is %s %s %s %r. The current time is %r %r AM" % (weekday, month, day, year, hour, min))
    elif hour >= 12 and hour < 18:
        hour = hour -12
        speak("Good Afternoon, today is %s %s %s %r. The current time is %r %r PM" % (weekday,month, day, year, hour, min))
    else:
        speak("Good Evening, today is %s %s %s %r. The current time is %r %r PM" % (weekday,month, day, year, hour, min))

def speak(speak1):
    #init the pyttsx library
    engine = pyttsx3.init()
    #load the the specifed message
    engine.say(speak1)
    #speak the meassage
    engine.runAndWait()
    print(speak1)

def youtube():
    #api key
    api = 'AIzaSyClgySUTgw47Q9Iy0T23W-ujXcfr-FQ6pI'
    #call the api using googleapiclient
    youtube = build('youtube', 'v3', developerKey=api)
    type(youtube)
    #asked for the name of the channel
    speak("what is the name of the channel?")
    input1 = speechRecegnizer()
    speak("here are the latest videos from %s" % input1)
    #request all the content from the speicfied channel (returns Json)
    req = youtube.search().list(q=input1, part='snippet', type='video')
    type(req)
    #execute the request
    res = req.execute()
    #print the title of the videos
    for item in res['items']:
        print(item['snippet']['title'])

def weather():
    #open weather api address
    api_address = 'http://api.openweathermap.org/data/2.5/weather?q=New%20York&units=imperial&appid=0c42f7f6b53b244c78a418f4f181282a'
    #request the json data from api address
    json_data = requests.get(api_address).json()
    #filter the json data for needed information
    high = json_data['main']['temp_max']
    low = json_data['main']['temp_min']
    feels_like = json_data['main']['feels_like']
    temp = json_data['main']['temp']
    format_add = json_data['weather'][0]['description']
    #speak the weather
    speak("The tempurture is %r degrees Fahrenheit and it feels like %r. With a high of %r and a low of %r. The current weather in Queens, New York is %s" % (temp, feels_like, high, low, format_add))

def stock_tracker(stock1):
    #get stock information using yahoo finance library
    stock1 = yf.Ticker(stock1)
    print(stock1.history(period="open"))

def briefing():
    #speak the date and time
    date_time()
    #open engadget
    webbrowser.open("engadget.com")
    speak("here are the latest news from engadget")
    #speak the weather
    weather()
    #open my email
    webbrowser.open("https://mail.google.com/mail/u/1/?tab=wm&ogbl#inbox")
    #tell me the current prices on these two stocks
    speak("here is the current price on VTI and VGT")
    stock_tracker('VTI')
    stock_tracker('VGT')

def email():
    recipients = []
    file1 = open("gmail user.txt", "r")
    f = file1.readlines()
    usernames = []
    usernames.extend(f)
    print(usernames)
    pick_user = int(input("pick a username: "))
    print(usernames[pick_user])
    passwords = []
    file2 = open("gmail pass.txt","r")
    f2 = file2.readlines()
    passwords.extend(f2)
    print(passwords)
    pick_password = int(input("pick a password: "))
    print(passwords[pick_password])
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.starttls()
    mail.ehlo()
    mail.login(usernames[pick_user], passwords[pick_password])
    mail.set_debuglevel(1)
    message = MIMEMultipart()
    text = MIMEText(input("Enter the message: "))
    message.attach(text)
    image = input("would you like to attach an image? ")
    if 'y' in image:
        name = input("enter the name of the image and the extension: ")
        img_data = open(name, 'rb').read()
        i = MIMEImage(img_data, name=os.path.basename(name))
        message.attach(i)
    sender = usernames[pick_user]
    file3 = open('recipient.txt','r')
    f3 = file3.readlines()
    recipients.extend(f3)
    print(recipients)
    r = int(input("choose a recipient: "))
    recipient = [recipients[r]]
    message['Subject'] = 'sent from python'
    message['From'] = sender
    message['To'] = ", ".join(recipient)
    mail.sendmail(sender, recipient, message.as_string())
    speak("email sent")

def text_me(message):
    try:
        #send email to my phone
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.starttls()
        mail.ehlo()
        mail.login('errorhandlerforai@gmail.com', 'familly01')
        mail.set_debuglevel(1)
        sender = 'errorhandlerforai@gmail.com'
        recipients = [""]
        msg = MIMEText(message)
        msg['Bcc'] = sender
        msg['To'] = ", ".join(recipients)
        mail.sendmail(sender, recipients, msg.as_string())
        print("email sent")
        #if the username or password arent accepted
    except smtplib.SMTPAuthenticationError:
        speak("username and password not accepted")

def main():
    if __name__ == "__main__":
        while True:
            my_command1 = speechRecegnizer()
            #open the google website
            if "Google" in my_command1:
                webbrowser.open('google.com')

            #if youtube is the command it calls youtube funtion
            if "YouTube" in my_command1:
               youtube()

            if "email" in my_command1:
                email()
            if "website" in my_command1:
                speak('please enter a url: ')
                url = speechRecegnizer()
                url = url + '.com'
                webbrowser.open(url)
                speak("now opening %s..." % url)
            #if shutdown is in the command it exits the program
            if "shutdown" in my_command1:
                speak("shutting down...")
                exit(0)
            #close all chorme prosess
            if "close Chrome" in my_command1:
                path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
                os.system('TASKKILL /F /IM chrome.exe')
                speak("chrome has been closed")
            #open a new chrome window
            if "open Chrome" in my_command1:
                path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
                app = subprocess.Popen(path)
                speak("here is chrome")
            #close all zoom prosess
            if "close Zoom" in my_command1:
                path = 'C:/Program Files (x86)/Zoom/bin'
                os.system('TASKKILL /F /IM Zoom.exe')
                speak("Zoom has been closed")
            #open a zoom window
            if "open Zoom" in my_command1:
                path = 'C:/Program Files (x86)/Zoom/bin/Zoom.exe'
                app = subprocess.Popen(path)
                speak("here is Zoom")
            #if the word weather is in the command it call the weather function
            if "weather" in my_command1:
                weather()
            #find the ip of the computer
            if "IP" in my_command1:
                hostname = socket.gethostname()
                IPAddr = socket.gethostbyname(hostname)
                speak("Your Computer Name is:" + hostname)
                speak("Your Computer IP Address is:" + IPAddr)
            #text me a specified message
            if "text me" in my_command1:
                speak("speak your message: ")
                message = speechRecegnizer()
                print(message)
                text_me(message)
            #find information on a specied stock
            if "stock" in my_command1:
                speak("Enter the stock symbol: ")
                stock1= speechRecegnizer()
                stock_tracker(stock1)
            #lock the computer
            if "lock" in my_command1:
                speak("locking now...")
                cmd = 'rundll32.exe user32.dll, LockWorkStation'
                subprocess.call(cmd)
            #call breifing function if its in the command
            if "briefing" in my_command1:
                briefing()
            #speak the date and time if the word "date" is in the command
            if "date" in my_command1:
                date_time()


main()
