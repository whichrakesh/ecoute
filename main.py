import threading
from AudioTranscriber import AudioTranscriber
from GPTResponder import GPTResponder
import customtkinter as ctk
import AudioRecorder 
import queue
import time
import torch
import sys
import TranscriberModels
import subprocess

def write_in_textbox(textbox, text):
    textbox.delete("0.0", "end")
    textbox.insert("0.0", text)

def update_response_UI(responder, textbox, freeze_state):
    if not freeze_state[0]:
        response = responder.response

        textbox.configure(state="normal")
        write_in_textbox(textbox, response)
        textbox.configure(state="disabled")

    textbox.after(300, update_response_UI, responder, textbox, freeze_state)

def clear_context(transcriber, audio_queue):
    transcriber.clear_transcript_data()
    with audio_queue.mutex:
        audio_queue.queue.clear()


def create_ui_components(root):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    root.title("Sage.AI")
    root.configure(bg='#252422')
    root.geometry("300x1080")

    font_size = 20

    response_textbox = ctk.CTkTextbox(root, width=300, font=("Arial", font_size), text_color='#639cdc', wrap="word")
    response_textbox.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

    freeze_button = ctk.CTkButton(root, text="Freeze", command=None)
    freeze_button.grid(row=1, column=0, padx=10, pady=3, sticky="nsew")
    return  response_textbox,  freeze_button


def main():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("ERROR: The ffmpeg library is not installed. Please install ffmpeg and try again.")
        return

    root = ctk.CTk()
    response_textbox, freeze_button = create_ui_components(root)

    audio_queue = queue.Queue()

    user_audio_recorder = AudioRecorder.DefaultMicRecorder()
    user_audio_recorder.record_into_queue(audio_queue)

    time.sleep(2)

    speaker_audio_recorder = AudioRecorder.DefaultSpeakerRecorder()
    speaker_audio_recorder.record_into_queue(audio_queue)

    model = TranscriberModels.get_model('--api' in sys.argv)

    transcriber = AudioTranscriber(user_audio_recorder.source, speaker_audio_recorder.source, model)
    transcribe = threading.Thread(target=transcriber.transcribe_audio_queue, args=(audio_queue,))
    transcribe.daemon = True
    transcribe.start()

    responder = GPTResponder()
    respond = threading.Thread(target=responder.respond_to_transcriber, args=(transcriber,))
    respond.daemon = True
    respond.start()

    print("READY")

    root.grid_rowconfigure(0, weight=100)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(0, weight=2)

    freeze_state = [False]  # Using list to be able to change its content inside inner functions
    def freeze_unfreeze():
        freeze_state[0] = not freeze_state[0]  # Invert the freeze state
        freeze_button.configure(text="Unfreeze" if freeze_state[0] else "Freeze")

    freeze_button.configure(command=freeze_unfreeze)
    
    update_response_UI(responder, response_textbox, freeze_state)
 
    root.mainloop()

if __name__ == "__main__":
    main()