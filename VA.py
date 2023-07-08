import speech_recognition
import pyttsx3
from datetime import date, datetime
import requests
import webbrowser
import time as ti

#Initial
robot_ear = speech_recognition.Recognizer()
robot_mouth = pyttsx3.init()
rate = robot_mouth.getProperty('rate') 
robot_mouth.setProperty('rate', 180)
voices = robot_mouth.getProperty("voices")
robot_mouth.setProperty("voice", voices[0].id)

def wake_VAP(cmd):
	wake_list = ['hey boy','hey bro', 'hello','wake up']
	for i in wake_list:
		if i in cmd:
			return True
	return False

def turn_off(cmd):	
	off_list = ['turn off','later','goodnight','go away','shutdown']
	for i in off_list:
		if i in cmd:
			robot_speak('Have a good day Sir, see you soon')
			return True
	return False

def standby_mode(cmd):
	wait_list = ['thank you', 'goodbye', 'ok, thanks','got it']
	for i in wait_list:
		if i in cmd:
			return True
	return False

def weather(city):	
	#CITY = "Ho Chi Minh City, VN"
	API_KEY = "5d6c28a3de83e2280b2497c8674bc0f5"
	URL = "https://api.openweathermap.org/data/2.5/weather?" + "q=" + city + " &appid=" + API_KEY
	response = requests.get(URL)
	data = response.json()
	try:
		ma = data['main']
		temperature = int(ma['temp'])-273
		report = data['weather']
		fi_report=report[0]['description']
		return [temperature, fi_report]
	except:
		return [0,0]

def time():
	time = datetime.now().strftime ("%R")
	if datetime.now().hour > 12:
		meri = ' P.M'
	else:	
		meri = ' A.M'
	return [time, meri]

def to_day():
	day = date.today().strftime	("%a %B %d")
	return day

def train_brain(cmd_text):
	if  cmd_text == '':
		robot_brain = "Can not understand"
	elif 'time' in cmd_text:																								
		robot_brain = 'what time is it now'
	elif 'today' in cmd_text:
		robot_brain = "which today"
	elif standby_mode(cmd_text) == True:
		robot_brain = 'come to stand by mode'
	elif 'weather' in cmd_text:
		robot_brain = 'how weather now'
	elif cmd_text!= '':
		robot_brain = cmd_text + 'search'
	else:
		robot_brain = ''
	return robot_brain

def action(robot_brain):
	if robot_brain == 'Can not understand':
		print ('Sorry I can not get you, please try again')
		robot_speak('Sorry I can not get you, please try again')
		
	elif robot_brain == 'what time is it now':
		x = time()
		print ('It is '+ str(x[0])+''+str(x[1]))
		robot_speak('It is '+ str(x[0])+''+str(x[1]))
		
	elif robot_brain == 'which today':
		x = to_day()
		print ('Today is '+ x)
		robot_speak('Today is '+ x)
		
	elif robot_brain == 'how weather now':
		x = [0,0]
		while x==[0,0]:
			robot_speak('weather for where?')
			ci = robot_hear()
			x = weather(ci)
		print('It is curently '+ str(x[1])+'. '+ 'Temperature now is '+ str(x[0]))
		robot_speak('It is curently '+ str(x[1])+'. '+ 'Temperature now is '+ str(x[0]))
	
	elif robot_brain == 'come to stand by mode':
		print('Goodbye, standby mode on, please say Hello to wake up')
		robot_speak ('Goodbye, standby mode on, please say Hello to wake up')

	elif 'search' in robot_brain:
		robot_brain = robot_brain[:-6]
		url = f'https://google.com/search?q={robot_brain}'
		robot_speak(f'Here is your {robot_brain} What I found for you')
		webbrowser.get().open(url)
		ti.sleep(7)
	else:
		pass


def robot_hear():
	with speech_recognition.Microphone() as mic:
		print('VOID: I am Hearing')
		robot_ear.adjust_for_ambient_noise(mic)
		audio = robot_ear.listen(mic,phrase_time_limit = 5)
	try:
		cmd_init = robot_ear.recognize_google(audio,show_all=True)
		data = cmd_init.get('alternative')
		cmd_text=''
		if len(data)<=1:
			cmd_text=data[0].get('transcript')
		else:
			for i in range (len(data)-1):
				x=data[i]
				x1=x.get('transcript')
				cmd_text = cmd_text +' '+ x1
	except:
		cmd_text=''
	print('You:'+ cmd_text)
	return cmd_text

def greeting():
	hour= datetime.now().hour
	if hour>=6 and hour <12:
		robot_brain = 'Good morning Sir. How can I help you?'
	elif hour>=12 and hour <18:
		robot_brain = 'Good afternoon Sir. How can I help you?'
	elif hour>=18 and hour <=24:
		robot_brain = 'Good evening Sir. How can I help you?'
	else:
		robot_brain = 'It is ' + str(hour) +' , Sir, How Can I help you?'
	print (robot_brain)
	return robot_brain

def robot_speak(z: str):
	robot_mouth.say(z)
	robot_mouth.runAndWait()
	robot_mouth.stop()

print ('I am V O I D,  your asistant, please say Hello')
robot_speak('I am V O I D,  your asistant, please say Hello')
while True:	
	cmd_text = robot_hear()
	if wake_VAP(cmd_text) == True:	
		robot_speak(greeting())
		x= 0
		while True:
			cmd = robot_hear()
			robot_brain = train_brain(cmd)
			action(robot_brain)
			if robot_brain == 'Can not understand':
				x = x+1
			if x >= 4:
				action('come to stand by mode')
				break
			if robot_brain == 'come to stand by mode':
				break
	if turn_off(cmd_text) == True:
		break