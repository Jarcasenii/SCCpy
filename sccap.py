import customtkinter
import subprocess
import pytube
import youtube_downloader
from tkinter import filedialog
import os
from tkinter import *
import moviepy.editor as mp
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageTk
import speechsr
from moviepy.editor import VideoFileClip


    

class VideoAudioConverter:
    def __init__(self, root):
        self.root = root

    def browsepc(self):
        self.file_name = filedialog.askopenfilename(title="Select a File", filetypes=(("Video files", "*.mp4*"),))
        self.convert(os.path.basename(self.file_name))

    def convert(self, path):
        clip = mp.VideoFileClip(r'{}'.format(path))
        clip.audio.write_audiofile(r'{}wav'.format(path[:-3]))


    
def convert_to_wav(filename):
    clip = VideoFileClip(filename)
    clip.audio.write_audiofile(filename[:-4] + ".wav")
    clip.close()

def youtubedl():
    links = youtube_downloader.input_links()
    for link in links:
        print("Downloading...")
        filename = youtube_downloader.download_video(link)
        print("Converting...")
        convert_to_wav(filename)

def snip():
    subprocess.call(["python", "snipping_tool.py"])

def quit_window(icon, item):
   icon.stop()
   root.destroy()

# Define a function to show the window again
def show_window(icon, item):
    icon.stop()
    root.after(1,root.deiconify)

# Hide the window and show on the system taskbar

def hide_window():
   root.withdraw()
   image=Image.open("faviconsc.ico")
   menu=(item('Close SCC', quit_window), item('Open SCC', show_window), item('Youtube Link', VideoAudioConverter(root).browsepc),item('Youtube Link',youtubedl), item('Capture',snip))
   icon=pystray.Icon("name", image, "ScreenCharaCaption", menu)
   icon.run()
  
def transcribe():
    path = filedialog.askopenfilename(title="Select a File", filetypes=(("Audio Files", "*.wav"),))
    text = speechsr.get_large_audio_transcription(path)
    text_file = open("data.txt", "w")
    text_file.write(text)
    text_file.close()
def clip():
    subprocess.call(["python", "clippy.py"])
       
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("400x550")
root.title("ScreenCharaCaption")
root.protocol('WM_DELETE_WINDOW', hide_window)

frame1 = customtkinter.CTkFrame (master=root)
frame1.pack(pady=20, padx=60, fill="x", expand=True)

label = customtkinter.CTkLabel(master=frame1, text="Speech Recognition")
label.pack(pady=12, padx=10)
button = customtkinter.CTkButton (master=frame1, text="Upload From PC", command=VideoAudioConverter(root).browsepc)
button.pack(pady=12, padx=10)
button = customtkinter.CTkButton (master=frame1, text="Youtube Link", command=youtubedl)
button.pack(pady=12, padx=10)
button = customtkinter.CTkButton (master=frame1, text="Transcribe", command=transcribe)
button.pack(pady=12, padx=10)
frame2 = customtkinter.CTkFrame (master=root)
frame2.pack(pady=20, padx=60, fill="x", expand=True)

label = customtkinter.CTkLabel(master=frame2, text="Character Recognition")
label.pack(pady=12, padx=10)
button = customtkinter.CTkButton (master=frame2, text="Capture", command=snip)
button.pack(pady=12, padx=10)
button = customtkinter.CTkButton (master=frame2, text="Clipboard", command=clip)
button.pack(pady=12, padx=10)

root.mainloop()
