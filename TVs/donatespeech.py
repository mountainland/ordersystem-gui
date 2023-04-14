import tkinter as tk
import requests
import sounddevice as sd
import soundfile as sf
import threading
import uuid


class SpeechDonorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Speech Donor")
        master.geometry("300x300")

        self.label = tk.Label(master, text="Please donate your speech to AI research")
        self.label.pack(pady=10)

        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.submit_button = tk.Button(master, text="Submit Recording", command=self.submit_recording, state=tk.DISABLED)
        self.submit_button.pack(pady=5)

    def start_recording(self):
        self.frames = []
        self.stream = sd.InputStream(channels=1, callback=self.record_audio)
        self.stream.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_recording(self):
        self.stream.stop()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.NORMAL)

    def record_audio(self, indata, frames, time, status):
        self.frames.append(indata.copy())

    def submit_recording(self):
        t = threading.Thread(target=self.upload_recording)
        t.start()

    def upload_recording(self):
        file_id = str(uuid.uuid4())
        file_name = f"recording_{file_id}.wav"
        sf.write(file_name, self.frames, 44100)

        self.label.config(text=f"Recording saved with ID: {file_id}")
        self.submit_button.config(state=tk.NORMAL)


root = tk.Tk()
app = SpeechDonorGUI(root)
root.mainloop()