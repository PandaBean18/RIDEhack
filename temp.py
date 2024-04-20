from gtts import gTTS
import pyttsx3
import datetime
import speech_recognition as sr


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 130)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 4:
        speak("Its Midnight!")
    elif 4 <= hour < 10:
        speak("Good Morning!")
    elif 10 <= hour < 16:
        speak("Good Afternoon!")
    elif 16 <= hour < 20:
        speak("Good Evening!")
    else:
        speak("Good Night!")

    engine.runAndWait()

    speak("I am Jarvis. How may I help you?")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("Recognising...")
        query = r.recognize_google(audio, language='en-in')
        print(query)

    except Exception as e:
        print("Say that again please...")
        return "None"

    return query

def jarvis(query):
    if 'hello' in query:
        speak("Hello")
    elif 'speak' in query:
        query = query.replace('speak', " ")
        speak(query)
    else:
        print(" ")
        speak("Error!")

if __name__ == "__main__":
    #wish_me()
    print("Start")
    while True:
        query = takecommand().lower()
        jarvis(query)