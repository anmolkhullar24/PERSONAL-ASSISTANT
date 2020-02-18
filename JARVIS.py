import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
from googlesearch import search
from googlesearch import search_images
from googlesearch import search_videos
import requests
import json
#from googlesearch.googlesearch import GoogleSearch

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def getWeather():
    api_address='http://api.openweathermap.org/data/2.5/weather?appid=bdc9b33ca5938b515a1e13e80b0ef589&q=zirakpur'
    json_data = requests.get(api_address).json()
    format_add = json_data['weather'][0]['description']
    return format_add


def wishMe():
    hour = int(datetime.datetime.now().hour)
    weather=getWeather()
    if hour>=0 and hour<12:
        speak("Good Morning ! You are the rising star")
        


    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
        

    else:
        speak("Good Evening!")
          

    speak("I am Jarvis Sir. today The Weather will be "+weather+" , Please tell me how may I help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    #print(sr.Microphone.list_microphone_names())
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1) 
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        if not mute:
            speak("Searching")
        
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e) 
        if not mute:
        	speak("Say that again please...")

          
        return False
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your email id', 'your login code')
    server.sendmail('your email id', to, content)
    server.close()

URL = 'https://www.way2sms.com/api/v1/sendCampaign'

# get request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
	req_params = {
	'apikey':apiKey,
	'secret':secretKey,
	'usetype':useType,
	'phone': phoneNo,
	'message':textMessage,
	'senderid':senderId
	}
	return requests.post(reqUrl, req_params)



if __name__ == "__main__":
    wishMe()
    mute = False
    while True:
    # if 1:
        
        query = takeCommand()
        while not query and not mute:
            speak("Listening")
            query = takeCommand()
        # Logic for executing tasks based on query
        while mute and not query:
        	query=takeCommand()
        query = query.lower()
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)


        elif 'search youtube' in query:
            speak("what would you like to search")
            query = takeCommand()
            while not query:
                speak("please say")
                query = takeCommand()
            query = query.lower()    
            query = query.replace(" ","+")
            webbrowser.open_new("www.youtube.com/results?search_query=" + query)

        elif ('search' or 'google') in query:
            print(query)
            query  = query.replace('search',"")
            query  = query.replace(' in google',"")
            query  = query.replace(' on google',"")
            query  = query.replace('images',"")
            query  = query.replace('videos',"")

            if 'images' in query:
            	speak("Searching images in google")
            	speak("These are the top 3 results")
            	for j in search_images(query,num=10, stop=3, pause=2):
                	print(j)
                	webbrowser.open_new(j)

            elif 'videos' in query:
            	speak("Searching videos in google")
            	speak("These are the top 3 results")
            	for j in search_videos(query,num=10, stop=3, pause=2):
                    print(j)
                    webbrowser.open_new(j)

            else:
                #for j in search(query, tld="co.in", num=10, stop=3, pause=2):
                #    print(j)
                #    speak("These are the top 3 results")
                #    webbrowser.open_new(j)
                speak("Searching"+query+"in google")
                query = query.replace(" ","+")
                webbrowser.open_new("https://www.google.com/search?q="+query)
                speak("these are the search results")


        elif 'open stackoverflow' in query:
            webbrowser.open_new("www.stackoverflow.com")
            speak("opened stackoverflow") 


        elif ('play'or' music') in query:
            music_dir = 'E:\\SONGS\\new'
            songs = os.listdir(music_dir)
            #print(songs)    
            for i in range(13):
            	os.startfile(os.path.join(music_dir, songs[i]))

            

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open' and 'code' in query:
            codePath = "C:\\Program Files\\Sublime Text 3\\sublime_text.exe"
            os.startfile(codePath)
            speak("Sublime Text has been opened")

        elif 'send mail' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak("Please say the email id")
                to = takeCommand().lower()
                to = to.replace(" ","")    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend harry bhai. I am not able to send this email")    
        elif ' shutdown jarvis '  in query:
            speak("Good bye sir! ALL The Best")
            os.system("shutdown /s /t 1") 
            quit()
        elif ("mute" or "mute jarvis") == query:
        	mute = True
        	speak("mute mode is on")
        elif 'unmute' in query:
        	mute = False
        	speak("Hello Sir Welcome Back hope you are having a good time")
        elif 'goodbye jarvis' in query:
        	#os.system("shutdown.exe /h")  #to check commands in cmd type :shutdown.exe /? 
        	speak("Good Bye sir")
        	quit()
        elif  'send message' in query:
            x = True
            while  x:
                speak("speak number to whome you want to send")
                number = takeCommand()
                number = number.replace(" ", "")
                speak("is  this  the correct number ?" + number)
                x = takeCommand()
            
                if x == 'yes':
                    speak("enter the message you want to send")
                    messages = takeCommand()
                    response = sendPostRequest(URL, 'your code', 'your code', 'prod', number, 'your email id', messages )
                    print (response.text)
                    speak("message sent")
                    x = False
                else:
                    continue

            
        else:
        	speak("Sorry i can't find the command ,please try again")

