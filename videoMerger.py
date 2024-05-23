# This script uses ffmpeg to quickly merge an mp3 file with an mp4 file. 
# The  part of the following code is done with the help of ChatGPT.

# Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
# choco install ffmpeg

import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import subprocess

def handle_dropped_file(event):
    file_path = event.data.strip('{}')  # Remove curly braces added by tkinterdnd2
    if os.path.isfile(file_path):
        if app.state == 'video' and file_path.lower().endswith('.mp4'):
            app.video_file = file_path
            app.label.config(text=f"Video file: {file_path}\n\nNow drag and drop the audio file.")
            app.state = 'audio'
        elif app.state == 'audio' and file_path.lower().endswith('.mp3'):
            app.audio_file = file_path
            app.label.config(text=f"Audio file: {file_path}\n\nProcessing files...")
            process_files()
        else:
            app.label.config(text="Invalid file. Please drag and drop a valid MP4 video or MP3 audio file.")
    else:
        app.label.config(text="Invalid file. Please drag and drop a valid file.")

def process_files():
    if app.video_file and app.audio_file:
        # Extract the directory from the audio file path
        output_dir = os.path.dirname(app.audio_file)
        output_path = os.path.join(output_dir, 'Combined.mp4')

        # Combine video and audio using ffmpeg
        command = [
            'ffmpeg',
            '-i', app.video_file,
            '-i', app.audio_file,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            output_path
        ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        app.label.config(text=f"Mission completed!\nCombined video saved as '{output_path}'.")

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Drag and Drop Video and Audio Combiner")
        self.geometry("600x200")
        self.label = tk.Label(self, text="Drag and drop the MP4 video file here.", pady=20)
        self.label.pack(expand=True)
        self.state = 'video'
        self.video_file = None
        self.audio_file = None
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', handle_dropped_file)

if __name__ == "__main__":
    app = App()
    app.mainloop()
