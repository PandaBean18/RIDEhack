import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
from gtts import gTTS
import pyttsx3
import random
import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 130)
project_id = "integral-hold-420817"
location = "us-central1"
vertexai.init(project=project_id, location=location)
model = GenerativeModel("gemini-1.0-pro")
chat = model.start_chat()
model_follow_up = model.start_chat()
chat_follow_up = model.start_chat()
points = 0
questions = []

default_responses = [
    "Interesting perspective, I appreciate that.",
    "That's a thoughtful response.",
    "Great, let's move on to the next question.",
    "Good to know, let's continue.",
    "Your input is valuable, thank you.",
    "Your response gives me good context, thanks.",
    "I understand, thank you for explaining.",
    "Insightful answer, thank you for sharing.",
    "Your insights are valuable.",
    "Your answer gives me good context.",
    "Your perspective is valued.",
    "Your response is noted.",
    "Your input helps guide the discussion.",
    "Your input helps us move forward.",
    "Your perspective helps shape our understanding.",
    "Your insights contribute to our understanding.",
    "Your perspective broadens our viewpoint.",
    "Your input enhances our understanding.",
    "Your perspective deepens our analysis.",
    "Your contribution moves us forward.",
    "Your insights contribute to our collective knowledge."
]

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

def initialize(chat: ChatSession):
    job_role = "The job role is " + "Backend flask developer" #input("Please enter the job role: ")
    past_exp = "My past experience is " + "I created an application called compass which helped users find their route using public transport based on a number of metrics such as cost, eco friendliness and time taken, it was built in flask" #input("What is your past experience?\n")
    get_chat_response(chat, job_role)
    get_chat_response(chat, past_exp)
    global questions 
    questions = get_chat_response(chat, "Give me the 5 questions, do not add any markdown, no numbering, no pretext, just the questions").split("\n")

def get_follow_up(chat, answers):
    prompt = "The answers for the questions are:\n"
    for i in range(len(answers)):
        prompt += "{}".format(i+1)
        prompt += answers[i]
        prompt += "\n"
    prompt += "Based on these ask follow up questions if you have any. Please try to keep the number of questions to a minimum, do not add any markdown, no numbering, no pretext, just the questions"
    questions = get_chat_response(chat, prompt).split("\n")
    return questions
    
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
    prompt = "this is my answer for {} is: ".format(index) + answer + ". Return strictly an integer grading this answer based on my knowledge of topic from 1-10. Just an integer, no explanation"
    grade = get_chat_response(chat, prompt)
    for a in range(len(grade)):
        if (grade[a] in "0123456789"):
            grade = grade[a]
            break
    return grade



initialize(chat)
questions = parse_questions(questions)
score = 0
answers = []
for i in range(len(questions)):
    if (questions[i] == ''):
        continue
    print(questions[i])
    speak(questions[i])
    answer = takecommand()
    answers.append(answer)
    response = random.choice(default_responses)
    speak(response)
    grade = process_answer(chat, answer, i)
    score += int(grade)


follow_up_questions = get_follow_up(chat, answers)
for i in range(len(follow_up_questions)):
    if (follow_up_questions[i] == ''):
        continue
    print(follow_up_questions[i])
    speak(follow_up_questions[i])
    answer = input("> ")


review = get_chat_response(chat, "On the basis of our interactions, Please let me know what i should improve upon.")

print(review)
speak(review)
print("Final score: {}/50".format(score))