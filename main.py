import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
import multiprocessing
from gtts import gTTS
import pyttsx3
import datetime
import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 130)


class Process(multiprocessing.Process):
    def __init__(self, chat, answer, index):
        super(Process, self).__init__() 
        self.chat = chat
        self.answer = answer
        self.index = index+1

    def get_chat_response(self, chat: ChatSession, prompt: str) -> str:
        text_response = []
        responses = chat.send_message(prompt, stream=True)
        for chunk in responses:
            text_response.append(chunk.text)
        
        return "".join(text_response)

    def get_follow_up(self):
        prompt = "Answer for {} is: ".format(self.index) + answer + "If you have a follow up question, ask it, else strictly return only 0, nothing else"
        follow = get_chat_response(self.chat, self.prompt)
        if (follow != "0"):
            return follow 
        else:
            return 0
        
    def run(self):
        get_follow_up()

# TODO(developer): Update and un-comment below lines
project_id = "integral-hold-420817"
location = "us-central1"
vertexai.init(project=project_id, location=location)
model = GenerativeModel("gemini-1.0-pro")
chat = model.start_chat()
model_follow_up = model.start_chat()
chat_follow_up = model.start_chat()
points = 0

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

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

def get_chat_response(chat: ChatSession, prompt: str) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

prompt = "You are an interviewer now. i will give you some information. when asked, give me 5 questions based on job role and my past experience."
print(get_chat_response(chat, prompt))

questions = []

def initialize(chat: ChatSession):
    job_role = "The job role is " + "Backend flask developer" #input("Please enter the job role: ")
    past_exp = "My past experience is " + "I created an application called compass which helped users find their route using public transport based on a number of metrics such as cost, eco friendliness and time taken, it was built in flask" #input("What is your past experience?\n")
    get_chat_response(chat, job_role)
    get_chat_response(chat, past_exp)
    global questions 
    questions = get_chat_response(chat, "Give me the 5 questions, do not add any markdown, no numbering, no pretext, just the questions").split("\n")

def parse_questions(questions):
    i = 0
    for question in questions:
        try:
            idx = question.index('.') + 1
            q = question[idx:-1]
            que = ""
            for x in q:
                if (x not in "*/\#"):
                    que += x
            questions[i] = q
            i += 1
        except: 
            next
    return questions

def process_answer(chat, answer, index):
    prompt = "this is my answer for {} is: ".format(index) + answer + ". Return strictly an integer grading this answer from 1-10. Just an integer, no explanation"
    grade = get_chat_response(chat, prompt)
    return grade



initialize(chat)
questions = parse_questions(questions)
score = 0
for i in range(len(questions)):
    if (questions[i] == ''):
        continue

    print(questions[i])
    speak(questions[i])
    answer = input("> ")
    grade = process_answer(chat, answer, i)
    score += int(grade)
    print("grade: {}".format(grade))

review = get_chat_response(chat, "On the basis of our interactions, Please let me know what i should improve upon.")

print(review)
speak(review)
print("Final score: {}/50".format(score))