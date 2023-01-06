# ==== Importing all the necessary libraries
from tkinter import *
from tkinter import filedialog
import os
from PIL import ImageTk
import moviepy.editor as mp

# ==== creating main class
class VideoAudioConverter:
    # ==== creating gui window
    def __init__(self, root):
        self.root = root
        self.root.title("VIDEO-AUDIO CONVERTER")


        Button(self.root,text="Browse Files",font=("times new roman", 15),command=self.browse).place(x=40, y=630)

    def browse(self):
        self.file_name = filedialog.askopenfilename(title="Select a File", filetypes=(("Video files", "*.mp4*"),))
        self.convert(os.path.basename(self.file_name))

    # ==== convert video to audio
    def convert(self, path):
        clip = mp.VideoFileClip(r'{}'.format(path))
        clip.audio.write_audiofile(r'{}wav'.format(path[:-3]))

# ==== creating main function
def main():
    # ==== create tkinter window
    root = Tk()
    # === creating object for class VideoAudioConverter
    obj = VideoAudioConverter(root)
    # ==== start the gui
    root.mainloop()

if __name__ == "__main__":
    # ==== calling main function
    main()