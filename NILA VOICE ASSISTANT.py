import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
import requests
import wikipedia
import webbrowser
import pywhatkit
import sys
import time
import threading
import ctypes
import math


# Initialize the pyttsx3 engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set voice to female

# Text-to-speech function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Convert voice to text function
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=7)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Could you try again?")
            return "none"
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception:
        speak("Say that again, please...")
        return "none"
    return query

# Check for internet connection
def check_internet():
    try:
        requests.get('https://www.google.com', timeout=3)
        return True
    except requests.ConnectionError:
        return False

# Function to wish the user
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning friend")
    elif hour > 12 and hour < 18:
        speak("Good Afternoon friend")
    else:
        speak("Good Evening friend")
    speak("I am Nila. Please tell me how I can help you.")

# Function to send WhatsApp message
def send_whatsapp_message():
    # Ask for the phone number
    speak("To whom should I send the message? Please provide the phone number with the country code, starting with plus.")
    phone_number = takecommand().strip()

    # Validate phone number
    if not phone_number.startswith("+"):
        speak("The phone number must include the country code, for example, plus nine one for India. Please try again.")
        return

    # Ask for the message
    speak("What should I say?")
    message = takecommand()

    # Validate message content
    if message.lower() == "none" or message.strip() == "":
        speak("No message was provided. Please try again.")
        return

    # Send the message
    try:
        if not check_internet():
            speak("Please turn on your internet connection before sending a WhatsApp message.")
            return
        speak("Sending your message now.")
        pywhatkit.sendwhatmsg_instantly(phone_number, message)
        speak("Message sent successfully!")
    except pywhatkit.core.exceptions.CountryCodeException:
        speak("The phone number is missing the country code. Please provide the full number, starting with plus.")
    except Exception as e:
        speak("Sorry, I couldn't send the message. Please try again.")
        print(f"Error: {e}")
    
# Function to search Google
def google_search(query):
    if check_internet():
        search_query = query.replace("search", "").replace("google", "").strip()
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        speak(f"Here are the Google search results for {search_query}")
    else:
        speak("Please turn on your internet connection.")    

# Function to open apps dynamically
def open_app(app_name):
    # Paths to popular applications
    paths = {
        "notepad": "C:\\Windows\\notepad.exe",
        "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    }
    if app_name in paths:
        os.startfile(paths[app_name])
        speak(f"Opening {app_name.capitalize()}")
    else:
        speak(f"Sorry, I couldn't find {app_name}. Please check if it's installed.")

# Set system volume function
def set_volume(volume_level):
    # Adjust system volume using ctypes (specific to Windows)
    ctypes.windll.user32.SetVolume(volume_level)
    speak(f"Volume set to {volume_level}%")

# Function for reminders
def reminder(message, delay):
    time.sleep(delay)
    speak(f"Reminder: {message}")

# List of jokes
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the computer go to the doctor? Because it had a virus!",
    "Why do programmers prefer dark mode? Because the light attracts bugs!"
]

# Dictionary of words
dictionary = {
    "python": "Python is a high-level programming language.",
    "nila": "Nila is your friendly voice assistant."
}

# Advanced calculation function
def advanced_calculate(expression):
    try:
        # Check for basic operations first
        if "plus" in expression or "add" in expression:
            numbers = [float(num) for num in expression.split() if num.replace('.', '', 1).isdigit()]
            result = numbers[0] + numbers[1]
        elif "minus" in expression or "subtract" in expression:
            numbers = [float(num) for num in expression.split() if num.replace('.', '', 1).isdigit()]
            result = numbers[0] - numbers[1]
        elif "multiply" in expression or "times" in expression:
            numbers = [float(num) for num in expression.split() if num.replace('.', '', 1).isdigit()]
            result = numbers[0] * numbers[1]
        elif "divide" in expression or "divide by" in expression:
            numbers = [float(num) for num in expression.split() if num.replace('.', '', 1).isdigit()]
            result = numbers[0] / numbers[1]
        elif "power" in expression or "raised to" in expression:
            base, exp = [float(num) for num in expression.split() if num.replace('.', '', 1).isdigit()]
            result = math.pow(base, exp)
        elif "square root" in expression:
            number = float([num for num in expression.split() if num.replace('.', '', 1).isdigit()][0])
            result = math.sqrt(number)
        elif "sine" in expression:
            angle = float([num for num in expression.split() if num.replace('.', '', 1).isdigit()][0])
            result = math.sin(math.radians(angle))
        elif "cosine" in expression:
            angle = float([num for num in expression.split() if num.replace('.', '', 1).isdigit()][0])
            result = math.cos(math.radians(angle))
        elif "tangent" in expression:
            angle = float([num for num in expression.split() if num.replace('.', '', 1).isdigit()][0])
            result = math.tan(math.radians(angle))
        elif "log" in expression and "natural" in expression:
            number = float([num for num in expression.split() if num.replace('.', '', 1).isdigit()][0])
            result = math.log(number)
        elif "log" in expression:
            number = float([num for num in expression.split() if num.replace('.', '', 1).isdigit()][0])
            result = math.log10(number)
        elif "factorial" in expression:
            number = int([num for num in expression.split() if num.replace('.', '', 1).isdigit()][0])
            result = math.factorial(number)
        elif "modulus" in expression or "mod" in expression:
            numbers = [int(num) for num in expression.split() if num.isdigit()]
            result = numbers[0] % numbers[1]
        else:
            # If the above cases didn't match, try evaluating the expression directly
            result = eval(expression)
        
        speak(f"The result is {result}")
    except Exception as e:
        speak("Sorry, I couldn't calculate that.")
        print(f"Error: {e}")

# Function to list files and folders
def list_files(directory):
    try:
        files = os.listdir(directory)
        if files:
            speak(f"I found {len(files)} files in {directory}.")
            print(files)
        else:
            speak("No files found in this directory.")
    except Exception as e:
        speak("Sorry, I couldn't access that directory.")
        print(e)

# Function to open files
def open_file(directory, filename):
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        os.startfile(file_path)
        speak(f"Opening {filename}")
    else:
        speak("Sorry, I couldn't find that file.")

# Function to delete files
def delete_file(directory, filename):
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        speak(f"Deleted {filename}")
    else:
        speak("Sorry, I couldn't find that file to delete.")

# Function to create a new file
def create_file(directory, filename):
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'w') as f:
            f.write("")  # Creating an empty file
        speak(f"Created a new file named {filename} in {directory}")
    except Exception as e:
        speak(f"Sorry, I couldn't create the file. Error: {e}")
        
# Ask user to select directory and perform file operations
def select_directory():
    speak("Would you like to search in the Desktop folder or the Documents folder?")
    query = takecommand().lower()

    # Default paths
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")


    if "desktop" in query:
        speak("You selected Desktop. Listing files on Desktop...")
        list_files(desktop_path)
    elif "documents" in query:
        speak("You selected Documents. Listing files in Documents...")
        list_files(documents_path)
    else:
        speak("Sorry, I didn't understand. Please say Desktop or Documents.")
        select_directory()

# Handle tasks based on commands
def handle_tasks(query):
    query = query.lower()

    if "open notepad" in query:
        open_app("notepad")
    elif "open command prompt" in query:
        os.system("start cmd")
        speak("Opening Command Prompt")
    elif "open edge" in query or "open microsoft edge" in query:
        open_app("edge")
    elif "send message" in query or "send a whatsapp message" in query:
        send_whatsapp_message()
    elif "open camera" in query:
        cap = cv2.VideoCapture(0)
        speak("Opening camera. Press Escape to close.")
        while True:
            ret, img = cap.read()
            cv2.imshow('webcam', img)
            k = cv2.waitKey(50)
            if k == 27:  # Press 'Esc' to exit the camera window
                break
        cap.release()
        cv2.destroyAllWindows()
        speak("Camera closed.")
    elif "open music" in query:
        music_dir = "E:\\songs"
        songs = os.listdir(music_dir)
        if songs:
            song = random.choice(songs)
            os.startfile(os.path.join(music_dir, song))
            speak(f"Playing {song}")
        else:
            speak("I couldn't find any songs in your music directory.")
    elif "ip address" in query:
        if check_internet():
            ip = requests.get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")
        else:
            speak("Please turn on your internet connection.")
    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        if check_internet():
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
                print(results)
            except:
                speak("I couldn't find any results on Wikipedia.")
        else:
            speak("Please turn on your internet connection.")
    elif "open youtube" in query:
        if check_internet():
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")
        else:
            speak("Please turn on your internet connection.")
    elif "joke" in query:
        speak(random.choice(jokes))
    elif "calculate" in query:
        expression = query.replace("calculate", "").strip()
        advanced_calculate(expression)
    elif "files" in query or "folders" in query:
        speak("What directory would you like to search in?")
        directory = takecommand()
        list_files(directory)
    elif "change directory" in query:
        speak("Which directory would you like to change to?")
        directory = takecommand()
        os.chdir(directory)
        speak(f"Changed directory to {directory}")
    elif "search" in query or "google" in query:
        google_search(query)
    elif "exit" in query:
        speak("Goodbye!")
        sys.exit()

if __name__ == "__main__":
    wish()

    while True:
        query = takecommand().lower()
        handle_tasks(query)
