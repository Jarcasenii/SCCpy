import customtkinter
import subprocess
import tkinter
from tkinter import filedialog, messagebox, Label
import os
import time
from PIL import Image
import moviepy as mp


class App(customtkinter.CTk):
    
    def __init__(self):

        def convert():
            filename = filedialog.askopenfilename(title="Select a File", filetypes=(("Audio or Video Files", "*.wav , *.mp4"),))
            patha = filename
            subprocess.call(['ffmpeg','-i',patha,'-acodec','pcm_s16le','-ac','1','-ar','16000','out.wav'])
        
        def transcribe():   
            myprocess = subprocess.Popen(['python','speechtotext.py'])
            mywindow = tkinter.Toplevel()
            mywindow.geometry("200x50")
            
            Label(mywindow, text = "Running...").place(x = 0,y = 0) 
            
            messagebox.showinfo(title="Process Loading..", message="Process is ongoing, wait for window to return.")
            self.withdraw()
            
            def check_process():
                if myprocess.poll() is None:
                    mywindow.after(100, check_process)
                else:
                    mywindow.destroy()
            check_process()  
            
            while myprocess.poll() is None:
                time.sleep(0.1)
                
            self.deiconify()
            
            self.speech_frame_textbox.insert("0.0","Ctrl + V to paste screenshotted text")
            
        def snip():
            myprocess = subprocess.Popen(["python", "snipping_tool.py"])
            mywindow = tkinter.Toplevel()
            mywindow.geometry("200x50")
            
            Label(mywindow, text = "Running...").place(x = 0,y = 0) 
            
            messagebox.showinfo(title="Process Loading..", message="Process is ongoing, wait for window to return.")
            self.withdraw()
            
            def check_process():
                if myprocess.poll() is None:
                    mywindow.after(100, check_process)
                else:
                    mywindow.destroy()
            check_process()  
            
            while myprocess.poll() is None:
                time.sleep(0.1)
                
            self.deiconify()
                 
            self.ocr_frame_textbox.insert("0.0","Ctrl + V to paste screenshotted text")
        
        def save1():
            f = open("demofile1.txt", "w")
            files = [('Text Document', '*.txt'),
             ('Word Document', '*.doc'), 
             ('PDF File', '*.pdf')]
            f = filedialog.asksaveasfile(mode='w', defaultextension=files, filetypes=files)
            text2save = self.speech_frame_textbox.get(0.0,"end")
            f.write(text2save)
            f.close()
        
        def save2():
            f = open("demofile2.txt", "w")
            files = [('Text Document', '*.txt'),
             ('Word Document', '*.doc'), 
             ('PDF File', '*.pdf')]
            f = filedialog.asksaveasfile(mode='w', defaultextension=files, filetypes=files)
            text2save = self.ocr_frame_textbox.get(0.0,"end")
            f.write(text2save)
            f.close()
             
        super().__init__()

        self.title("uTranscribe")
        self.geometry("1080x720")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo_single.png")), size=(55, 50))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.speech_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "speech_light.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "speech_dark.png")), size=(20, 20))
        self.ocr_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "ocr_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "ocr_light.png")), size=(15, 20))
       
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  uTranscribe", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.speech_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Speech Recognition",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.speech_image, anchor="w", command=self.speech_button_event)
        self.speech_button.grid(row=2, column=0, sticky="ew")

        self.ocr_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Character Recognition",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.ocr_image, anchor="w", command=self.ocr_button_event)
        self.ocr_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_label = customtkinter.CTkLabel(self.home_frame, text="Welcome to \nuTranscribe!",
                                                  font=customtkinter.CTkFont(size=30, weight="bold"))
        self.home_label.grid(row=1, column=0, padx=20, pady=10)
        tabview_1 = customtkinter.CTkTabview(self.home_frame, width=1280, height=300)
        tabview_1.grid(pady=10, padx=10)
        tabview_1.add("Speech Recognition")
        label = customtkinter.CTkLabel(master=tabview_1,
                               text="This feature will allow you to convert Speech from videos to a text format. \n\nUpload video button lets the user upload a video from the PC, \nor paste a YouTube link lets the user paste a video link from YouTube. \n\n Transcribe button lets you transcribe the file you chose. \n\n Save file to .txt lets you save your file to a .txt format.",
                               width=10,
                               height=10,
                               font=customtkinter.CTkFont(size=18, weight="normal"))
        label.place(relx= 0.5, rely=0.5, anchor=tkinter.CENTER)
        
        tabview_2 = customtkinter.CTkTabview(self.home_frame, width=1280, height=200)
        tabview_2.grid(pady=10, padx=10)
        tabview_2.add("Character Recognition")
        label = customtkinter.CTkLabel(master=tabview_2,
                               text="This feature will allow you to select a part of your screen to take a screenshot and extract the text from it. \n\nCapture button lets the user take a screenshot. \n\nSave file to .txt lets you save your file to a .txt format.",
                               width=10,
                               height=10,
                               font=customtkinter.CTkFont(size=18, weight="normal"))
        label.place(relx= 0.5, rely=0.5, anchor=tkinter.CENTER)
        # create speech frame
        self.speech_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.speech_frame.grid_columnconfigure(0, weight=1)
        self.speech_frame_button_upload=customtkinter.CTkButton(self.speech_frame, text="Upload Video or audio", image=self.image_icon_image, compound="top",command=convert)
        self.speech_frame_button_upload.grid(row=1, column=0, padx=20, pady=10)
        self.speech_frame_button_yt = customtkinter.CTkButton(self.speech_frame, text="or paste a YouTube link")
        self.speech_frame_button_yt.grid(row=2, column=0, padx=20, pady=10)
        self.speech_frame_button_yt = customtkinter.CTkButton(self.speech_frame, text="Transcribe Video", command=transcribe)
        self.speech_frame_button_yt.grid(row=3, column=0, padx=20, pady=10)
        self.speech_frame_textbox = customtkinter.CTkTextbox(self.speech_frame, height=500)
        self.speech_frame_textbox.grid(row=4, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.speech_frame_save_as = customtkinter.CTkButton(self.speech_frame, text="Save As", command=save1)
        self.speech_frame_save_as.grid(row=5, column=0, padx=20, pady=10)
        
        self.ocr_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.ocr_frame.grid_columnconfigure(0, weight=1)
        self.ocr_frame_button_upload=customtkinter.CTkButton(self.ocr_frame, text="Capture Image", image=self.image_icon_image, compound="top",command=snip)
        self.ocr_frame_button_upload.grid(row=1, column=0, padx=20, pady=10)
        self.ocr_frame_textbox = customtkinter.CTkTextbox(self.ocr_frame, height=500)
        self.ocr_frame_textbox.grid(row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.ocr_frame_save_as = customtkinter.CTkButton(self.ocr_frame, text="Save As", command=save2)
        self.ocr_frame_save_as.grid(row=3, column=0, padx=20, pady=10)
        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.speech_button.configure(fg_color=("gray75", "gray25") if name == "speech" else "transparent")
        self.ocr_button.configure(fg_color=("gray75", "gray25") if name == "ocr" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "speech":
            self.speech_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.speech_frame.grid_forget()
        if name == "ocr":
            self.ocr_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.ocr_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def speech_button_event(self):
        self.select_frame_by_name("speech")

    def ocr_button_event(self):
        self.select_frame_by_name("ocr")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
