import ctypes
from customtkinter import*
import hashlib
from PIL import Image
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

Users = ['shayan-safari-dev']
Passwords = ['03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4']

version = 'v1.1'

my_app_id = 'Mr. AI' + version
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

username = None

def check_password(id):
    global username_original

    print('Checking password',id)
    hasher = hashlib.sha256()
    # Using SHA-256
    hashed = hasher.update(str(password_to_check).encode('utf-8'))
    #print(hasher.hexdigest()) 
    hashed = hasher.hexdigest()
    if Passwords[id] == hashed:
        print("loged in")
        login_window.destroy()

    else:
        print("worng password")
        login_window.destroy()
        username_original = 'shayan'

def login_check():
    
    global password_to_check, username_original

    password_to_check = password_entry.get().lower()
    username = user_entry.get().lower()
    username_original = user_entry.get()
    print("Password to check is: ***", ' User:', username)
    for i in range(len(Users)):
        if Users[i] == str(username):
            print('checking user :', i, Users[i])
            check_password(i) 

        else:
            print('No accounts was found!')

#Login window - UI
def login():
    
    global password_entry
    global user_entry, is_hidden
    global login_window, login_frame
    global transparent, id

    #window
    transparent = "#FAFAFA"

    login_window = CTk()
    login_window.geometry('600x500')
    login_window.configure(fg_color=transparent)
    login_window.title("Login")
    
    border_width = 2.5
    id = 0

    is_hidden = True

    def hide():
        global is_hidden

        if is_hidden == True:
            password_entry.configure(show = '')
            hide_btn.configure(image = CTkImage(show_btn_image, size=(30,32)))
        else:
            password_entry.configure(show = '•')
            hide_btn.configure(image = CTkImage(hide_btn_image, size=(30,32)))
        is_hidden = not is_hidden
            
    #Design

    login_frame = CTkFrame(login_window, height=500 , width=500, border_color="#FF6666",
                           border_width=0, fg_color=transparent)
    login_frame.place(anchor = CENTER, relx = 0.5, rely = 0.52)

    logo()

    login_lable = CTkLabel(login_window, text="Login", font=('arial',50,'bold'), text_color="#DFDFDF",bg_color=transparent)

    user_entry = CTkEntry(login_frame, placeholder_text_color="#C4C4C4", placeholder_text="username",font=('arail',22),
                          width=430, height=61, corner_radius=30, border_width= border_width,
                          text_color="#303030", bg_color=transparent, fg_color= "#FFFFFF",
                          border_color='#C4C4C4')
    
    password_entry = CTkEntry(login_frame, placeholder_text_color="#C4C4C4", placeholder_text="password",font=('arail',22),
                          width=430, height=61, corner_radius=30, border_width= border_width, 
                          text_color="#303030", bg_color=transparent, fg_color= "#FFFFFF",
                          border_color="#C4C4C4", show = '•')
    
    login_button = CTkButton(login_frame, text_color="white", text="Login",font=('arail',24),
                          width=430, height=61, corner_radius=30, command= lambda : login_check(), 
                          bg_color=transparent, fg_color= "#232323", hover_color="#383838") #334E52
    

    hide_btn_path = os.path.join(BASE_DIR, "design", "buttons", "hide.png")
    hide_btn_image = Image.open(hide_btn_path)

    show_btn_path = os.path.join(BASE_DIR, "design", "buttons", "show.png")
    show_btn_image = Image.open(show_btn_path)

    hide_btn = CTkButton(password_entry, text_color="white", text="",
                          width=38, height=38, corner_radius=0, command= lambda: hide(),
                          bg_color=transparent, fg_color="#FFFFFF", hover_color="#FFFFFF",
                          image= CTkImage(hide_btn_image, size=(30,32)))

    #login_lable.place(anchor = 'center', relx=0.5, rely=0.18)

    user_entry.place(anchor = 'center', relx= 0.5 ,rely= 0.4)
    password_entry.place(anchor = 'center', relx = 0.5 , rely = 0.55)
    hide_btn.place(anchor = CENTER, x = 390, rely = 0.5)

    login_button.place(anchor = 'center', relx = 0.5 , rely = 0.75)

    login_window.bind("<Return>", lambda e: login_check())

    login_window.mainloop()

def logo():

    #Low resulution
    logo_path = os.path.join(BASE_DIR, "design", "logo", "Transparent logo.ico")
    login_window.iconbitmap(logo_path)

    #logo--------------------------------------
    #High resulution
    logo_path = os.path.join(BASE_DIR, "design", "logo", "Transparent logo.png")
    logo_img = Image.open(logo_path) #IMPORTANT - Not logo_path
    logo_screen = CTkLabel(login_frame, 
                        image=CTkImage(light_image=logo_img, size=(100,100)), text="")

    logo_screen.place(relx = 0.5, y=30, anchor=CENTER)

    app_name = CTkLabel(login_frame, text="Welcome Back", font=("Inter", 36,'bold'), 
                        fg_color=transparent, text_color="#334E52")
    app_name.place(relx = 0.498, y=120, anchor=CENTER)

login()