import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_trending_movies, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message, note, send_whatsapp_image , calender
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_discord
from random import choice
from utils import opening_text
from pprint import pprint
from instabot import Bot
from datetime import date
import gui
import threading



import httplib2
import os
import googleapiclient.discovery as discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from tkinter import simpledialog


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json


USERNAME = config('USER')
BOTNAME = config('BOTNAME')


engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""
    engine.say(text)
    gui.speak(text)
    engine.runAndWait()


# Greet the user
def greet_user():
    """Greets the user according to the time"""
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")


# Takes Input from User
def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
    
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    
    try:
        
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir, take care!")
            else:
                speak('Have a good day sir!')
            exit()
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query

def main():
    def commands():
        query = take_user_input().lower()

        if 'open notepad' in query:
            open_notepad()

        elif 'open discord' in query:
            open_discord()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(
                f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            speak('What do you want to search on Wikipedia, sir?')
            search_query = take_user_input().lower()
            try:
                results = search_on_wikipedia(search_query)
                speak(f"According to Wikipedia, {results}")
                speak("For your convenience, I am printing it on the screen sir.")
                print(results)
            except Exception:
                speak("Sorry, sir canoot process your request!!")

        elif 'youtube' in query:
            speak('What do you want to play on Youtube, sir?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'play a song' in query or 'play song' in query or "play" in query:
            speak('What do you want to play on , sir?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'search on google' in query or "search" in query:
            speak('What do you want to search on Google, sir?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "send whatsapp message" in query or "send what's up message" in query or "whatsapp" in query:
            speak(
                'On what number should I send the message sir? Please enter in the console: ')
            number = simpledialog.askstring(title="Number", prompt="Enter Phone Number :")
            speak("What is the message sir?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message sir.")

        elif "send an email" in query or "write email" in query or "send email" in query or "email" in query:
            speak("On what email address do I send sir? Please enter in the console: ")
            receiver_address = simpledialog.askstring(title="Reciever's Address", prompt="Enter receiver's Email Address :")
            speak("What should be the subject sir?")
            subject = take_user_input().capitalize()
            speak("What is the message sir?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("I've sent the email sir.")
            else:
                speak(
                    "Something went wrong while I was sending the mail. Please check the error logs sir.")

        elif 'joke' in query:
            speak(f"Hope you like this one sir")
            joke = get_random_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen sir.")
            pprint(joke)

        elif "advice" in query:
            speak(f"Here's an advice for you, sir")
            advice = get_random_advice()
            speak(advice)
            speak("For your convenience, I am printing it on the screen sir.")
            pprint(advice)

        elif "trending movies" in query:
            speak(f"Some of the trending movies are: {get_trending_movies()}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_trending_movies(), sep='\n')

        elif 'news' in query:
            speak(f"I'm reading out the latest news headlines, sir")
            speak(get_latest_news())
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_latest_news(), sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(
                f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(
                f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")

        elif "spell the word" in query:
            word = query.replace("spell the word", " ")
            print(f"spelling of the word {word} is", end=" ")
            speak(f"spelling of the word {word} is")
            for i in word:
                print(i, end=" ")
                speak(i)

        elif "Check my internet connection" in query or "internet avilablity" in query or "internet connection" in query:
            url = "http://www.kite.com"
            timeout = 5
            try:
                request = requests.get(url, timeout=timeout)
                print("Connected to the Internet")
                speak("Connected to the Internet")
            except (requests.ConnectionError, requests.Timeout) as exception:
                print("No internet connection.")
                speak("No internet connection.")

        elif "note" in query:
            speak("What would you like me to write down?")
            note_text = take_user_input().lower()
            note(note_text)
            speak("I've made a note of that.")

        elif "send message on insta" in query:
            speak('What you would like to message sir?')
            bot = Bot()

            bot.login(username="whoharshfulzele88",
                      password="Harsh@123")
            speak("Enter Recivers username sir in the console sir")
            receiver_address = simpledialog.askstring(title="Reciever's Address : ", prompt="Enter receiver username : ")
            speak("What is message sir?")
            message = take_user_input().lower()

            bot.send_message(message, [receiver_address])
            speak("message has been sent sir")

        elif "message on insta" in query:
            speak('What you would like to post sir?')
            bot = Bot()

            bot.login(username="whoharshfulzele88", password="Harsh@123")
            speak("Enter Recivers username sir in the console")
            receiver_address = simpledialog.askstring(title="Reciever's Address : ", prompt="Enter receiver username : ")            
            speak('what is the message sir')
            message = take_user_input().lower()
            bot.send_message(message, [receiver_address])
            speak("message has been sent sir")

        elif "send image" in query:
            speak(
                'On what number should I send the image sir? Please enter in the console: ')
            number = simpledialog.askstring(title='Enter Number', prompt="Enter Phone Number : ")
            speak("Select image sir")
            img_path = "F:\CP\Files\py files\Virtual-Personal-Assistant-using-Python-master\Virtual-Personal-Assistant-using-Python-master"
            send_whatsapp_image(number, img_path)
            speak("I've sent the image sir.")

        elif "date" in query :
            today = date.today()
            now = datetime.now()
            now1 = now.strftime("%H:%M:%S %b %d %Y")
            speak(f"Today's time and  date is  {now1}")
            speak("For your convenience, I am printing it on the screen sir.")
            print("today :", now1)

        elif 'what is your name' in query or 'Name' in query or 'How can you help me?' in query :
            speak('I am Elvis. I am virtual assistant with various modules and submodules. I can search on web , send message on whatsapp , instagram , Email ,fetch the events from your primary calender and many more. Hope I will be helpfull for you sir. Thank you')
            print('I am Elvis. I am virtual assistant with various modules and submodules. I can search on web , send message on whatsapp , instagram , Email ,fetch the events from your primary calender and many more. Hope I will be helpfull for you sir. Thank you')
        
        elif 'How old are you?' in query or 'Whats your age?' in query or 'age' in query:
            speak('I am Elvis. I am virtual assistant with various modules and submodules. I am program so I dont have age ' )
            print('I am Elvis. I am virtual assistant with various modules and submodules. I am program so I dont have age ')

        elif 'Who made you?' in query or 'made' in query:
            speak('I made by Harsh , Jayesh and sushank. Thank you sir')
            print('I made by Harsh , Jayesh and sushank. Thank you sir')

        elif 'Tell me something' in query or 'tell me' in query:
            speak('would you like to search something on web, you can activate by saying serch on google sir. Thank you')
            print('would you like to search something on web, you can activate by saying serch on google sir. Thank you')

        elif 'Happy birthday' in query or 'birthday' in query:
            speak('would you like to play a birthday song , please say paly a song , beacuse I am program I dont have birthday sir')
            print('would you like to play a birthday song , please say paly a song , beacuse I am program I dont have birthday sir')
        
        elif 'Don’t you speak English?' in query or 'what language you speak?' in query or 'english' in query:
            speak('I only speak English sir.')

        elif 'What is your mother’s name?' in query or 'mother' in query:
            speak('I am a program sir')
            print('I am a program sir')

        elif 'Do you get smarter?' in query or 'smarter' in query:
            speak('I have predefine module where, I match you input data and send responce accordingly')
            print(
                'I have predefine module where, I match you input data and send responce accordingly')

        


        elif 'event' in query or 'events' in query:
            start , summary =calender()
           
            speak(f'{start} , {summary}')

        elif 'sleep' in query or 'lock' in query or 'turn off' in query or 'turn of' in query:
            speak('turning off your system sir. Thank you')
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


        else:
            
            speak('I am unable to understand sir, Would you like me to serch on Web? ')
            if 'yes' in take_user_input().lower() and 'none' not in query:         
                search_on_google(query)
            elif 'none' in query:
                speak("Sorry sir, unable to process your request, can you please try again!")

            else:
                speak('Ohhh... Please try again, sir!')
    
    t1 = threading.Thread(target=gui.set_speak_command(commands), args=())

    t2 = threading.Thread(target=gui.mainloop(), args=())

    t1.start()
    t2.start()
    
if __name__ == '__main__':
    greet_user()
    main()
    
    
    
        
            

    
