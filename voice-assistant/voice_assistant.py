import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import smtplib
import wikipedia
from email.mime.text import MIMEText

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Greet the user based on the time
def greetUser():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Alexa, your personal assistant. How can I assist you today?")

# Function to recognize speech input
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

# Function to open various websites
def openWebsite(query):
    websites = {
        'youtube': 'https://www.youtube.com',
        'google': 'https://www.google.com',
        'stack overflow': 'https://stackoverflow.com',
        'wikipedia': 'https://www.wikipedia.org',
        'spotify': 'https://open.spotify.com',
        'github': 'https://github.com',
    }
    for site in websites:
        if site in query:
            webbrowser.open(websites[site])
            speak(f"Opening {site} for you.")
            return True
    return False

# Function to tell the current time
def tellTime(query):
    if 'time' in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        return True
    return False

# Function to tell the current date
def tellDate(query):
    if 'date' in query:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today's date is {current_date}")
        return True
    return False

# Function to search for information on Wikipedia
def searchWikipedia(query):
    if 'search wikipedia for' in query:
        query = query.replace("search wikipedia for", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        return True
    return False

# Function to send email
def sendEmail(subject, body, to_email):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        # Add email credentials
        server.login('tmooro55@gmail.com', 'xyckbitlaztrigww')
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'John'
        msg['To'] = to_email
        server.sendmail('tmooro55@gmail.com', to_email, msg.as_string())
        server.quit()
        speak("Email sent successfully!")
    except Exception as e:
        print(e)
        speak("Sorry, I am unable to send the email at the moment.")


# Function to recognize email address
def extractEmailAddress(query):
    email = ""
    words = query.split()
    for word in words:
        if '@' in word:
            email = word.replace("at", "@").replace("dot", ".")
            break
    return email

# Main function
if __name__ == "__main__":
    greetUser()
    while True:
        query = takeCommand()
        
        # Open websites
        if openWebsite(query):
            continue
        
        # Get current time
        if tellTime(query):
            continue

        # Get current date
        if tellDate(query):
            continue

        # Search Wikipedia
        if searchWikipedia(query):
            continue

        # Get sent email    
        if 'send email' in query:
            speak("What should be the subject of the email?")
            subject = takeCommand()
            speak("What should I say in the email?")
            body = takeCommand()
            speak("Whom should I send this email to?")
            to_email = extractEmailAddress(takeCommand().lower())
            sendEmail(subject, body, to_email)
            continue

        # Quit the program
        if 'exit' in query or 'quit' in query:
            speak("Goodbye!")
            break

        # If no specific command is recognized
        speak("I'm sorry, I didn't catch that. Can you please repeat?")
