from tkinter import *
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
import os
import shutil

from gtts import gTTS
import pygame
from pypdf import PdfReader

root = ctk.CTk()
root.geometry("600x650")
root.title('My Audiobook App 📖')

ctk.set_appearance_mode('light') 
ctk.set_default_color_theme('dark-blue')

UPLOAD_FOLDER = "uploads"
is_paused = False
is_playing = False
audio_file = "audiobook.mp3"


def submit():
    global file_path, text
    file_path = filedialog.askopenfilename(title="Select a file",
                            filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        filename = os.path.basename(file_path)
        dest = os.path.join(UPLOAD_FOLDER, filename)
        shutil.copy(file_path, dest)
        CTkMessagebox(title="Info", message="File uploaded successfully!")
        
        if file_path:  
            reader = PdfReader(file_path)

            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        my_content.delete("1.0", "end")
        my_content.insert("1.0", text)
        my_button.configure(state="disabled")
        my_label.configure(text="✅ Your book is ready to read!")
        read_button.configure(state="normal")
        stop_button.configure(state="normal")
        

def read():
    global is_paused, is_playing
    
    read_button.configure(state="disabled")
    pause_button.configure(state="normal")
    stop_button.configure(state="normal")


    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
        return   
            
    tts = gTTS(text=text, lang='en', slow=False)
    
    if os.path.exists(audio_file):
        os.remove(audio_file)
        
    tts.save(audio_file)
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
        
                    
def pause():
    global is_paused
    
    read_button.configure(state="normal")
    pause_button.configure(state="disabled")
    stop_button.configure(state="normal")
    
    pygame.mixer.music.pause()
    is_paused = True
    

def stop():
    global is_paused, is_playing
    
    read_button.configure(state="disabled")
    pause_button.configure(state="disabled")
    stop_button.configure(state="disabled")
    my_button.configure(state="normal")
    my_label.configure(text="😄 Upload your preferred pdf file!")
    my_content.delete("1.0", "end")
    
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.quit()
    
    is_paused = False
    is_playing = False
    
    file_path = os.path.join("uploads", "audiobook.pdf")
    
    if os.path.exists(file_path):
        os.remove(file_path)
        CTkMessagebox(title="Info", message="File deleted successfully!")
    else:
        CTkMessagebox(title="Info", message="File does not exist!")
    
    
header = ctk.CTkLabel(root, text="Welcome to My Audiobook App 📖", 
                      font=('Roboto', 24),
                      text_color="#1a1a1a")
header.pack(pady=20)

my_frame = ctk.CTkFrame(root, height=300, width=500, corner_radius=15,
                        fg_color="#D2C8C8", 
                        border_width=2, border_color="#cccccc")
my_frame.pack(pady=30)

my_label = ctk.CTkLabel(my_frame, 
                        text="😄 Upload your preferred pdf file!",
                        width=500, height=40,
                        font=('Roboto', 16))
my_label.pack(pady=20)

my_button = ctk.CTkButton(my_frame, 
                          text="Submit your book",
                          width=150,
                          height=40,
                          command=submit)
my_button.pack(pady=20)

book_label = ctk.CTkLabel(root, text="Book content:", font=('Roboto', 16),
                          text_color="#1a1a1a")
book_label.pack(anchor=W, padx=50)

my_content = ctk.CTkTextbox(root, width=500, height=200,
                                font=('Roboto', 14), activate_scrollbars=True,
                            border_width=2, border_color="#cccccc")
my_content.pack(pady=10)

button_frame = ctk.CTkFrame(root, height=50, width=500, corner_radius=10)
button_frame.pack(pady=20)

book_image = CTkImage(
    light_image=Image.open("media/book.png"),
    size=(30, 30)
)

pause_image = CTkImage(
    light_image=Image.open("media/pause.png"),
    size=(30, 30)
)

stop_image = CTkImage(
    light_image=Image.open("media/stop.png"),
    size=(30, 30)
)
    
read_button = ctk.CTkButton(button_frame, 
                          text="Read",
                          image=book_image,
                          compound='left',
                          height=50,
                          width=100,
                          state="disabled",
                          command=read)
read_button.grid(row=0, column=0, padx=40, pady=10)

pause_button = ctk.CTkButton(button_frame, 
                          text="Pause",
                          image=pause_image,
                          compound='left',
                          height=50,
                          width=100,
                          state="disabled",
                          command=pause)
pause_button.grid(row=0, column=1, padx=40, pady=10)

stop_button = ctk.CTkButton(button_frame, 
                          text="Stop",
                          image=stop_image,
                          compound='left',
                          height=50,
                          width=100,
                          state="disabled",
                          command=stop)
stop_button.grid(row=0, column=2, padx=40, pady=10)

root.mainloop()
