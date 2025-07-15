# ✅ Required packages:
# pip install playsound==1.2.2
# pip show edge-tts

# voice_generator_gui.py
# Advanced Voice Generator GUI with inline explanations
# Author: Anshu Goel

import asyncio  # For asynchronous voice generation
import edge_tts  # Main TTS engine from Microsoft Edge
import tkinter as tk  # GUI toolkit
from tkinter import ttk, filedialog, messagebox  # Enhanced widgets & dialogs
from playsound import playsound  # For audio playback
import threading  # To prevent UI blocking during tasks
import os  # For file handling
from datetime import datetime  # To generate unique filenames

# Voice options mapped with human-readable names
voices = {
    "English (US) - Aria [Female]": "en-US-AriaNeural",
    "English (UK) - Libby [Female]": "en-GB-LibbyNeural",
    "English (IN) - Neerja [Female]": "en-IN-NeerjaNeural",
    "English (US) - Guy [Male]": "en-US-GuyNeural"
}

# Default output name & folder for generated voices
DEFAULT_OUTPUT = os.path.join("GeneratedVoices", "output_voice.mp3")
OUTPUT_FOLDER = "GeneratedVoices"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

# Maintain reference to the latest generated file
latest_generated_file = DEFAULT_OUTPUT

# Asynchronous audio generator using edge_tts
async def generate_audio(text, voice, output_file):
    communicator = edge_tts.Communicate(text=text, voice=voice)
    await communicator.save(output_file)  # Save TTS to file

# Wrapper function for generation + UI messaging
# Updates the global reference to latest_generated_file
def speak_text(text, voice, path):
    global latest_generated_file
    if not text.strip():
        messagebox.showwarning("Empty Text", "Please enter some text.")
        return
    asyncio.run(generate_audio(text, voice, path))
    latest_generated_file = path  # Update the latest generated file
    messagebox.showinfo("Done", f"MP3 Saved:\n{path}")

# Audio player using threading to avoid UI freeze
# Always plays the latest generated file
def play_audio():
    if os.path.exists(latest_generated_file):
        threading.Thread(target=playsound, args=(latest_generated_file,), daemon=True).start()
    else:
        messagebox.showwarning("Not Found", f"No audio file found at:\n{latest_generated_file}")

# GUI setup and main loop
def start_gui():
    root = tk.Tk()
    root.title("Anshu Goel's Pro Voice Generator GUI")
    root.geometry("800x600")

    # App Title
    title = tk.Label(root, text="🎙️ Anshu Goel's Voice Generator Pro", font=("Segoe UI", 16, "bold"))
    title.pack(pady=10)

    # Frame for text input + scrollbar
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=5)

    scroll = tk.Scrollbar(frame)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    text_box = tk.Text(frame, height=15, font=("Segoe UI", 12), wrap=tk.WORD, yscrollcommand=scroll.set)
    text_box.pack(side=tk.LEFT, fill="both", expand=True)
    scroll.config(command=text_box.yview)

    # Dropdown voice selector
    tk.Label(root, text="Select Voice:", font=("Segoe UI", 11)).pack(pady=(10, 3))
    voice_var = tk.StringVar(value=list(voices.keys())[0])
    voice_menu = ttk.Combobox(root, textvariable=voice_var, values=list(voices.keys()), state="readonly", width=50)
    voice_menu.pack()

    # Character count display
    word_count_label = tk.Label(root, text="Characters: 0", font=("Segoe UI", 10))
    word_count_label.pack(pady=(5, 0))

    # Update character count on key release
    def update_count(event=None):
        content = text_box.get("1.0", "end-1c")
        word_count_label.config(text=f"Characters: {len(content)}")
    text_box.bind("<KeyRelease>", update_count)

    # Generate MP3 and save it to a timestamped file
    def generate():
        text = text_box.get("1.0", "end").strip()
        voice = voices[voice_var.get()]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(OUTPUT_FOLDER, f"output_{timestamp}.mp3")
        threading.Thread(target=speak_text, args=(text, voice, path), daemon=True).start()

    # Play the most recently generated MP3 file
    def play():
        play_audio()

    # Save generated voice using a user-defined path
    def save():
        file = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if file:
            text = text_box.get("1.0", "end").strip()
            voice = voices[voice_var.get()]
            threading.Thread(target=speak_text, args=(text, voice, file), daemon=True).start()

    # Clear the input text area
    def clear():
        text_box.delete("1.0", "end")

    # Load content from a text file
    def load():
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file:
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
            text_box.delete("1.0", "end")
            text_box.insert("1.0", text)

    # Save typed script to a text file
    def export_script():
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(text_box.get("1.0", "end").strip())

    # Bottom panel for all main actions
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="🎧 Generate", command=generate, width=12).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="▶️ Play", command=play, width=10).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="💾 Save As MP3", command=save, width=15).grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="📂 Load Text", command=load, width=12).grid(row=0, column=3, padx=5)
    tk.Button(button_frame, text="📝 Export Script", command=export_script, width=14).grid(row=0, column=4, padx=5)
    tk.Button(button_frame, text="🧹 Clear Text", command=clear, width=12).grid(row=0, column=5, padx=5)

    # Footer credits
    tk.Label(root, text="© Anshu Goel 2025 | edge-tts powered", font=("Segoe UI", 9, "italic")).pack(pady=10)

    root.mainloop()  # Start GUI loop

# Launch GUI if script is run directly
if __name__ == "__main__":
    start_gui()
