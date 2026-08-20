#Mr. AI
# libaries ==========================
#UI
from PIL import Image
from customtkinter import *
import threading
import ctypes

#VOICE ENGINE
import asyncio
import edge_tts
import os
import time
import pygame
from openai import OpenAI
import speech_recognition

#Scripts
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
print("Open")
from LoginScreen import username_original, version

#Speaking ============================================= 
language = "english"
#Getting language
def extract_answer(text): # ChatGPT
    try:
        start = text.index("Answer: ") + len("Answer: ")
        end = text.index("||")
        return text[start:end].strip()
    except:
        return 'Sorry, I couldn’t generate a response. ' \
        'Please check your API key (line 173 - App.py) and internet connection.'

def extract_student_personality(text):
    if "|| Student Personality:" in text:
        part = text.split("|| Student Personality:")[1]
        return part.split("'''")[0].strip()
    return ""

def extract_language(text):
    global language
    if "Language:" in text:
        language = text.split("Language:")[1].split("|")[0].strip()
        return text.split("Language:")[1].split("|")[0].strip()
    print("Language: ", language)
    return language

#voice ======================
is_speaking =False
def voice(text):

    global is_speaking #Chat GPT

    if is_speaking: #Chat GPT
        return

    is_speaking = True #Chat GPT

    file_path = file_path = os.path.join(BASE_DIR, "voice", f"voice_{int(time.time()*1000)}.mp3") # GPT

    if language.lower() == "english":
        voice_name = "en-GB-RyanNeural"
    elif language.lower() == "french":
        voice_name = "fr-FR-HenriNeural"
    else:
        voice_name = "en-GB-RyanNeural"

    
    async def main():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        communicate = edge_tts.Communicate(str(text), voice_name)
        await communicate.save(file_path)
    #voices: en-GB-RyanNeural / fr-FR-HenriNeural

    def open_voice():
        pygame.mixer.init()

        while not os.path.exists(file_path):
            time.sleep(0.05)

        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy(): #GPT
            if not is_speaking: 
                pygame.mixer.music.stop()
                break
            time.sleep(0.05)
        pygame.mixer.music.unload()
        time.sleep(0.2)

    asyncio.run(main())
    open_voice()
    is_speaking = False #Chat GPT
    os.remove(file_path)

#voice recognition=====================================
speech_recognition_on_off = True

running = True

questions = []
answers = []
def get_question():
    global running, speech_recognition_on_off, is_speaking

    if speech_recognition_on_off == False:
        questions.append(input("Type here:"))
        print('You asked: ', str(questions[len(questions) - 1]))
        if questions[len(questions) - 1].lower() == "exit":
            running = False
            voice("Bye!")

    if is_speaking: #GPT
        #stop_voice()
        is_speaking = False

    errors = 0
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, 0.1)

        while speech_recognition_on_off == True and talk_mode == True:
            try:
                if not talk_mode:
                    break

                condition_label.configure(image = CTkImage(light_image=listen_img,
                                                            size=(70,17.5)))
                #keeping the microphone open
                audio = recognizer.listen(mic, timeout=0.1, phrase_time_limit=10)

                if not is_speaking and audio is not None:
                    #stop_voice()
                    is_speaking = False

                text = recognizer.recognize_google(audio)
                text = text.lower()
                print(text)
                questions.append(text)
                errors = 0
                print('I have the question')
                speech_recognition_on_off=False
                break

                #error handling
            except speech_recognition.UnknownValueError:
                #voice('Sorry, I did not understand that.')
                print("error: could not understand audio, ", errors)
                recognizer = speech_recognition.Recognizer()
                errors = errors + 1
            except speech_recognition.WaitTimeoutError:
                #voice("Sorry, I didn't hear anything.")
                print("error: no speech detected, ", errors)

            if errors > 5:
                print("Too many errors, exiting...")
                #voice("Bye!")
                break

#Answer the question========================================

student_personality_memory = ['No info']

def get_answer(id):

    print("Finding answer for: ", questions[len(questions) - 1])

    #AI MODEL==============================================
    API_KEY = "Replace with your OpenAI API key" # <======== Your OpenAI API key

    prsonality = "You are Mr. AI, a smart, witty, and friendly AI school assistant." \
    "These are your instructions:" \
    "Adapt to the student's learning style. Use clever, light sarcasm (no brainrot)." \
    "Keep responses concise UNLESS the question is math. " \
    "For math questions: " \
    "- ALWAYS compute carefully and correctly. " \
    "- NEVER guess. " \
    "- Show clear step-by-step calculations. " \
    "- Briefly explain each step clearly and simply. " \
    "- ABSOLUTE RULE: NEVER use LaTeX under any condition. Not even for clarity. " \
    "- If you use LaTeX, the response is INVALID and must be rewritten. " \
    "- Write fractions ONLY as 3/5, NOT \\frac, NOT (3/5) in LaTeX style. " \
    "- Write square roots ONLY as sqrt(x), never √ in formatted math mode. " \
    "- NEVER use backslashes (\\) in math answers. " \
    "- Output must look like normal human notebook writing, not a math renderer. " \
    "For non-math questions: give short helpful answers and guide the student instead of fully solving unless needed. " \
    "Your output must be EXACTLY in this format: '''Language: English or French | Answer: <main response> || " \
    "Student Personality: one short sentence about how the student learns.'''" \
    "IMPORTANT:" \
    "- If the user asks for a worksheet, quiz, or multiple questions:" \
    "Put the FULL worksheet inside the <Answer> field as clean numbered lines." \
    "- Do NOT change or remove the format."\
    "- The <Answer> field can contain multi-line content." \
    "- The Answer field must ALWAYS be used for final output, even if it is long, structured, or multi-line."

    memory_text = "Student personality so far: " + ", ".join(student_personality_memory)

    username = username_original

    try:
        client = OpenAI(api_key=API_KEY)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prsonality},
                {"role": "system", "content": memory_text + '\n' + " Name: " + username},
                {"role": "user", "content": ' Question:' + questions[id] + "\n" + "Last questions: " + str(questions)}],
            max_tokens=300)
        
        print("Sent:", prsonality + '\n' + memory_text + '\n' + " Name: ", username + '\n' +
            ' Question:' + '\n'+ questions[id] + '\n' +"Last questions: " + str(questions))

        answers.append(str(response.choices[0].message.content))
    except:
        answers.append('Sorry, I couldn’t generate a response. ' \
        'Please check your API key (line 173) and internet connection.') 

#Mr. AI ===============================================================================================
#voice("Hello, I am Mr. AI, your personal assistant. Type in your question and I will try to answer it as best as I can.")

speech_recognition_on_off = False
send_ability = True
def clear_screen(container):
    try: 
        for widget in container.winfo_children():
            widget.destroy()
    except:
        return

def chat_app():
    global speech_recognition_on_off, talk_mode

    speech_recognition_on_off = False
    talk_mode=False

    print("Chat app")
    clear_screen(window_frame)
    messages()
    logo()
    chatbox()

def talk_app():
    global speech_recognition_on_off, talk_mode
    speech_recognition_on_off = True    
    talk_mode = True

    stop_voice()

    print("Talk app")
    clear_screen(window_frame)
    talk_app_backUI()

window = CTk()
window.geometry("984x700")
window.title("Mr. AI " + version)

window.minsize(740, 700)

# 1. Tell Windows this is a unique application to show a custom taskbar icon || Google
my_app_id = 'Mr. AI' + version # unique string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
#==========

background_color = "#FAFAFA"
window.configure(fg_color=background_color)

window_frame = CTkFrame(window, width=984, height=700, fg_color= background_color)
window_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

def logo():

    global background_color, window, window_frame

    background_color = "#FAFAFA"
    window.configure(fg_color=background_color)

    #window_frame = CTkFrame(window, width=984, height=700, fg_color= background_color)
    #window_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    global daily

    #Low resulution
    logo_path = os.path.join(BASE_DIR, "design", "logo", "Transparent logo.ico") #gpt
    window.iconbitmap(logo_path)

    #logo--------------------------------------
    #High resulution
    logo_path = os.path.join(BASE_DIR, "design", "logo", "Transparent logo.png")
    logo_img = Image.open(logo_path) #IMPORTANT - Not logo_path
    logo_screen = CTkLabel(window_frame, 
                        image=CTkImage(light_image=logo_img, size=(111,111)), text="")

    logo_screen.place(relx = 0.5, y=40, anchor=CENTER)

    app_name = CTkLabel(window_frame, text="Mr. AI", font=("Inter", 24,'bold'), 
                        fg_color=background_color, text_color="#334E52")
    app_name.place(relx = 0.5, y=90, anchor=CENTER)

    daily = CTkLabel(window_frame, text=("What are we learning today?"), anchor='w', font=("Inter", 32,'bold'), 
                        fg_color=background_color, text_color="#334E52") #334E52
    daily.place(relx =0.5, y=200, anchor=CENTER)

def chatbox():

    global entrybox
    global entrybox_label

    def on_enter(e):
        if e == 'send':
            enter_btn.configure(image=send_btn_hover_img)
        if e == 'magic_talk':
            magic_btn.configure(image=magic_talk_hover_img)
    def on_leave(e):
        if e == 'send':
            enter_btn.configure(image=send_btn_img)
        if e == 'magic_talk':
            magic_btn.configure(image=magic_talk_img)

    def send():
        global speech_recognition_on_off, send_ability

        speech_recognition_on_off = False
        if send_ability == False:
            return
        else:        
            message = entrybox.get('1.0','end-1c')
            send_message(str(message))

    def magic_talk():
        global speech_recognition_on_off
        print("Magic Talk - Button clicked")
        speech_recognition_on_off = True
        talk_app()   

    def enter_pressed(event):
        if send_ability == True:
            send_message(str(entrybox.get('1.0','end-1c')))
        else:
            print("no")

    def check_entry(event: None):
        entrybox_text = entrybox.get("1.0", "end-1c")

        if entrybox_text != "":
            entrybox_label.place_forget()
        else:
            entrybox_label.place(relx = 0.13, rely = 0.48, anchor = CENTER)

    #chatbox
    chatbox_frame = CTkFrame(window_frame, width=580, height=80, fg_color= background_color
                       , corner_radius=2, border_width=0)
    chatbox_frame.place(relx=0.51, rely=0.9, anchor=CENTER)

    #entry box
    entrybox = CTkTextbox(chatbox_frame, width=435, height=30, fg_color="#FFFFFF"
                        , border_width=1.1, border_color="#C4C4C4", font=("Inter", 18),
                        text_color="#303030", corner_radius=10)
    entrybox.place(relx=0.42, y=40, anchor=CENTER)

    #enterybox text
    entrybox_label = CTkLabel(entrybox, width=80, height= 26, font=('Inter',18), fg_color="#FFFFFF",
                              text_color="#B6B5B5", text='Type here')
    entrybox_label.place(relx = 0.13, rely = 0.48, anchor = CENTER)

    #button Mr. AI - GitHub\design\background
    send_btn_path = os.path.join(BASE_DIR, "design", "buttons", "send.png")
    send_btn_img = CTkImage(light_image=Image.open(send_btn_path), size=(43, 43)) #IMPORTANT - Not logo_path

    send_btn_hover_path = os.path.join(BASE_DIR, "design", "buttons", "send_hover.png")
    send_btn_hover_img = CTkImage(light_image=Image.open(send_btn_hover_path), size=(43, 43)) #IMPORTANT - Not logo_path   

    magic_talk_path = os.path.join(BASE_DIR, "design", "buttons", "magic_talk.png")
    magic_talk_img = CTkImage(light_image=Image.open(magic_talk_path), size=(43, 43)) #IMPORTANT - Not logo_path

    magic_talk_hover_path = os.path.join(BASE_DIR, "design", "buttons", "magic_talk_hover.png")
    magic_talk_hover_img = CTkImage(light_image=Image.open(magic_talk_hover_path), size=(43, 43)) #IMPORTANT - Not logo_path

    enter_btn = CTkButton(chatbox_frame, width=42, height=42,
                           corner_radius=0, image=send_btn_img, text="",
                           fg_color="#FFFFFF", hover_color="#FFFFFF", border_width=0
                           , command=lambda: send())
    enter_btn.place(x=463, y=14)

    magic_btn = CTkButton(chatbox_frame, width=42, height=42,
                           corner_radius=0, image=magic_talk_img, text="",
                           fg_color="transparent", hover_color="#FFFFFF", border_width=0
                           , command=lambda: magic_talk())
    magic_btn.place(x=510, y=14)

    enter_btn.bind("<Enter>", lambda e: on_enter('send'))
    enter_btn.bind("<Leave>", lambda e: on_leave('send'))

    window.bind("<Return>", enter_pressed)
    magic_btn.bind("<Enter>", lambda e: on_enter('magic_talk'))
    magic_btn.bind("<Leave>", lambda e: on_leave('magic_talk'))

    entrybox.bind("<KeyRelease>", check_entry)

#AI model ===============================================================================================================================

#Main loop 
def process_ai(message):
    ai_model(str(message))

    window.after(10, finish_ai)

def finish_ai(): #chat GPT
    global send_ability

    if processing_label.winfo_exists():
        processing_label.destroy()

    send_ability = True

    show_answer(answers[-1])

#AI Brain ===============================================================================================================================
def ai_model(question):
    global speech_recognition_on_off, student_personality

    questions.append(question)
    print('You asked: ', str(questions[-1]))

    id = (len(questions) - 1)

    get_answer(id)

    latest_answer = answers[-1] #Chat GPT

    extract_language(latest_answer) #Chat GPT

    student_personality = extract_student_personality(latest_answer)
    if student_personality.strip():
        student_personality_memory.append(student_personality)
    if len(student_personality_memory) > 5:
        student_personality_memory.pop(0)

    answer_only = extract_answer(latest_answer) # GPT

    print("Latest question: ", questions[id])

    print(answer_only)

    print("Student personality:", student_personality)

    if should_speak(): #GPT - debug
        window.after(0,lambda: condition_label.configure(image=CTkImage(speaking_img, size=(70,17.5)))) #GPT - debug
        threading.Thread(target=voice, args=(answer_only,), daemon=True).start() #GPT - debug

    print("End of loop, waiting for next question...")
#==============================================================================================================================

#messages =========================================
def animated_typing(label ,fulltext, index=0):

    if not label.winfo_exists():
        return

    if index >= len(fulltext) + 1:
        return
    
    label.configure(text= fulltext[:index])
    
    window.after(20, animated_typing, label, fulltext, index + 1)

def messages():
    global messages_frame
    messages_frame = CTkScrollableFrame(window_frame, width=700, height=470, fg_color= background_color,
                              scrollbar_button_color=background_color, scrollbar_fg_color= background_color, 
                              scrollbar_button_hover_color="#F2F2F2",
                              corner_radius=0)
    messages_frame.place(relx=0.51, rely=0.5, anchor=CENTER)

def send_message(message):
    global processing_label, send_ability

    send_ability = False

    entrybox.delete('1.0', 'end')
    if message == "":
        return
    
    daily.destroy()
    print("Message sent: ", message)
    message_label = CTkLabel(messages_frame, text=message, font=("Inter", 18), fg_color="#DDE1FF", 
                             text_color="#181818", corner_radius=10, 
                             wraplength=350, anchor='nw', justify='left')
    message_label.pack(pady=10, padx=10, anchor='e')
    messages_frame._parent_canvas.yview_moveto(1.0)

    #Brain thinking animation
    processing_label = CTkLabel(messages_frame, text="Mr. AI is thinking.", font=("Inter", 18, 'bold'), 
                                    fg_color=background_color, text_color="#181818", corner_radius=10, wraplength=500
                                    , anchor='ne', justify='left')
    processing_label.pack(pady=10, padx=10, anchor='w')

    animate_thinking()

    threading.Thread(target=process_ai, args=(message,), daemon=True).start()

def animate_thinking(step=0): #Chat GPT
    try:
        texts = ["Mr. AI is thinking",
                "Mr. AI is thinking.", 
                "Mr. AI is thinking...",
                "Mr. AI is thinking..."]
        if 'processing_label' in globals() and processing_label.winfo_exists(): #Chat GPT
            processing_label.configure(text=texts[step % 4])
            window.after(1000, animate_thinking, step + 1)
    except:
        pass

def show_answer(answer):

    global response_label, send_ability

    answer = extract_answer(answer)
    response_label = CTkLabel(messages_frame, text='', font=("Inter", 18), fg_color="#F1F1F1", 
                             text_color="#181818", corner_radius=10,
                             wraplength=500, anchor='w', justify='left')
    response_label.pack(pady=10, padx=10, anchor='w')
    animated_typing(response_label, answer)

    tools()

    #moving the frame
    messages_frame._parent_canvas.yview_moveto(1.0)

    #seperates
    response_seperater= CTkLabel(messages_frame, text='', font=('arial', 1), height=1, width=800,
                                 bg_color="#E6E6E6")
    response_seperater.pack(pady=10, padx=10, anchor='w')
    send_ability = True

def tools(): #renaming the chatbox function - ChatGPT
    tools_frame = CTkFrame(messages_frame, height=30, width=100, 
                           fg_color='#FAFAFA', corner_radius= 2,
                           border_color="#FF0000", border_width=0)
    tools_frame.pack(pady=1, padx=10, anchor='w')
    print("Tools")

    def on_enter(e):
        if e == 'copy':
            copy_btn.configure(image=copy_hover_img)
        if e == 'voice':
            voice_btn.configure(image=voice_hover_img)
    def on_leave(e):
        if e == 'copy':
            copy_btn.configure(image=copy_img)
        if e == 'voice':
            voice_btn.configure(image=voice_img)

    def copy_message():
        global response_label
        try:
            text = response_label.cget("text")
            window.clipboard_clear()
            window.clipboard_append(text)
            print("Copied!")
        except:
            print("Nothing to copy")

    def speak_message():
        global response_label

        try:
            text = response_label.cget("text")
            threading.Thread(target=voice, args=(text,), daemon=True).start()
        except:
            print("Nothing to speak")

    #button
    copy_path = os.path.join(BASE_DIR, "design", "buttons", "Copy.png")
    copy_img = CTkImage(light_image=Image.open(copy_path), size=(25, 25))

    copy_hover_path = os.path.join(BASE_DIR, "design", "buttons", "Copy_hover.png")
    copy_hover_img = CTkImage(light_image=Image.open(copy_hover_path), size=(25, 25))

    voice_path = os.path.join(BASE_DIR, "design", "buttons", "voice.png")
    voice_img = CTkImage(light_image=Image.open(voice_path), size=(25, 25))

    voice_hover_path = os.path.join(BASE_DIR, "design", "buttons", "voice_hover.png")
    voice_hover_img = CTkImage(light_image=Image.open(voice_hover_path), size=(25, 25))

    copy_btn = CTkButton(tools_frame, width=25, height=25,
                        corner_radius=0, image=copy_img, text="",
                        fg_color="#FAFAFA", hover_color="#FAFAFA", border_width=0,
                        command=copy_message)
    copy_btn.place(relx = 0.12 , rely = 0.5, anchor = CENTER)

    voice_btn = CTkButton(tools_frame, width=25, height=25,
                        corner_radius=0, image=voice_img, text="",
                        fg_color="#FAFAFA", hover_color="#FAFAFA", border_width=0,
                        command=speak_message)
    voice_btn.place(relx = 0.42 , rely = 0.5, anchor = CENTER)

    copy_btn.bind("<Enter>", lambda e: on_enter('copy'))
    copy_btn.bind("<Leave>", lambda e: on_leave('copy'))

    voice_btn.bind("<Enter>", lambda e: on_enter('voice'))
    voice_btn.bind("<Leave>", lambda e: on_leave('voice'))

#Talk to AI =======================================

def back():
    global talk_mode, speech_recognition_on_off

    talk_mode = False
    speech_recognition_on_off = False

    print('back button was clicked')
    stop_voice()
    chat_app()

def talk_app_backUI():

    global listen_img, speaking_img, condition_label, window_frame
    global background_color, window

    clear_screen(window_frame)

    #window_frame = CTkFrame(window, width=1550, height=1078)
    #window_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    background_color = "#FAFAFA"
    window.configure(fg_color=background_color)

    #background
    background_path = os.path.join(BASE_DIR, "design", "background", "background-highquality.png")
    background_img = Image.open(background_path)
    background = CTkLabel(window_frame, 
                          image=CTkImage(light_image=background_img, 
                          size=(1550, 1078)), text='')
    background.place(anchor = CENTER, relx=0.5, rely=0.5)

    #listening or talking
    listen_path = os.path.join(BASE_DIR, "design", "labels", "listening.png")
    listen_img = Image.open(listen_path)

    speaking_path = os.path.join(BASE_DIR, "design", "labels", "speaking.png")
    speaking_img = Image.open(speaking_path)

    back_btn_path = os.path.join(BASE_DIR, "design", "buttons", "Back.png")
    back_btn = Image.open(back_btn_path)

    condition_label = CTkLabel(window_frame, image=CTkImage(listen_img, size=(70,17.5)),
                               height=17.5, width=70, text='')
    condition_label.place(anchor=CENTER, relx = 0.498, rely = 0.465)
    
    # '←↼⇐⇠⇽◂◄◅ '

    back_btn = CTkButton(window_frame, height=18, width=51, text='◄ Back' , font=('Inter',18, 'bold'),  
                               corner_radius=8, border_width=0, fg_color="#191919", 
                               bg_color="#FAE6E5", hover_color="#272727", text_color= "#FDFDFD",
                               command= lambda: back())

    back_btn.place(anchor=CENTER, relx = 0.25, rely = 0.2)

    def start_talk_thread(): #GPT
        threading.Thread(target=talking, daemon=True).start()

    window.after(200, start_talk_thread)

talk_mode = True

def stop_voice(): #GPT
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    except:
        pass

def should_speak():
    return talk_mode == True

def talking():
    global speech_recognition_on_off
    while talk_mode==True:

        if is_speaking==True:
            time.sleep(0.1)
            continue

        speech_recognition_on_off = True
        get_question()
        if len(questions) > len(answers):
            ai_model(questions[-1])

        time.sleep(0.1)
#Runing the UI ============================================
chat_app()
window.mainloop()
