# This script uses python3 to decode videos downloaded from bilibili client
# The  part of the following code is done with the help of ChatGPT.

# if the python library is missing try running the following command
# pip install moviepy
# pip install tkinterdnd2
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os

def removeFirstNBytes(input_file_path, output_file_path, n):
    with open(input_file_path, 'rb') as f:
        content = f.read()[n:]
    with open(output_file_path, 'wb') as f:
        f.write(content)

def handle_dropped_file(event):
    file_path = event.data.strip('{}')  # Remove curly braces added by tkinterdnd2
    if os.path.isfile(file_path):
        if app.state == 'video':
            app.video_file = file_path
            app.label.config(text=f"Video file: {file_path}\n\nNow drag and drop the audio file.")
            app.state = 'audio'
        elif app.state == 'audio':
            app.audio_file = file_path
            app.label.config(text=f"Audio file: {file_path}\n\nProcessing files...")
            process_files()
    else:
        app.label.config(text="Invalid file. Please drag and drop a valid file.")

def process_files():
    if app.video_file and app.audio_file:
        # Extract the directory from the audio file path
        output_dir = os.path.dirname(app.audio_file)
        video_output = os.path.join(output_dir, 'Output.mp4')
        audio_output = os.path.join(output_dir, 'Output.mp3')
        
        # Process video and audio files
        removeFirstNBytes(app.video_file, video_output, 9)
        removeFirstNBytes(app.audio_file, audio_output, 9)
        
        # Remove the input files
        os.remove(app.video_file)
        os.remove(app.audio_file)
        
        app.label.config(text=f"Mission completed!\nVideo saved as '{video_output}' and audio saved as '{audio_output}'.")

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Drag and Drop File Processor")
        self.geometry("600x200")
        self.label = tk.Label(self, text="Drag and drop the video file here.", pady=20)
        self.label.pack(expand=True)
        self.state = 'video'
        self.video_file = None
        self.audio_file = None
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', handle_dropped_file)

if __name__ == "__main__":
    app = App()
    app.mainloop()
