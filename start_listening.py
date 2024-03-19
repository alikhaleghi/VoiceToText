import speech_recognition as sr
import pyttsx3
import pyperclip
import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file (if it exists)
config.read('config.ini') 
  
# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
  """Converts text to speech and plays it"""
  engine.say(text)
  engine.runAndWait()

def listen(): 

  """Captures audio from microphone until a key is pressed"""
  with sr.Microphone() as source:
    print("Listening...")
    recognized_text = None
    try:
      listener = recognizer.listen(source )  # Set timeout to avoid infinite wait
      language = config.get('Settings', 'language')
      
      recognized_text = recognizer.recognize_google(listener, language=language)
      return recognized_text
        
    except sr.WaitTimeoutError:
      print("Speak Faster please!")
      recognized_text = listen()

    except sr.UnknownValueError:
      print("Could not understand audio")
    except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))

    if recognized_text:
      return recognized_text
# # Main loop
# while True:
#   text = listen()
#   if text:
#     speak(text)
