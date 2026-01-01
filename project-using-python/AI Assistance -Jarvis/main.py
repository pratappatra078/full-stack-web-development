import speech_recognition as sr 
import webbrowser
import pyttsx3
import time
import musicLibray
import requests


recognizer = sr.Recognizer()
engine = pyttsx3.init()

def processCommand(c):
    print(c)
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open reddit" in c.lower():
        webbrowser.open("https://www.reddit.com/?feed=home.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibray.music[song]
        print(link)
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/everything?q=tesla&from=2025-09-02&sortBy=publishedAt&apiKey=823c2d67dc1545b6903235756b1281b1")
        if r.status_code == 200:
            data = r.json()
            articals = data.get('articles',[])

            for article in articals:
                engine.say(article['title'])
    elif "open twitter" in c.lower():
        webbrowser.open("https://x.com/home")

def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    speak("initialising Jarvis......")
    while True:
        print("inside function..")
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source ,timeout=3,phrase_time_limit=5)
            word = r.recognize_google(audio)
            print(word)
            if (word.lower() == "jarvis"):
                engine.say("Ya")
                with sr.Microphone() as source:
                    print("Jarvis Activated ")
                    audio = r.listen(source )
                    command = r.recognize_google(audio)
                    processCommand(command)


        except Exception as e :
            print("Error;{0} ".format(e))