import streamlit as st
from pvrecorder import PvRecorder
import wave
import struct
import speech_recognition as sr


## Convert audio into text
def audio_to_text(): 
    recognizer = sr.Recognizer() 

    audio_path = "audio_recording.wav" 

    try: 
        with sr.AudioFile(audio_path) as source: 
            audio_data = recognizer.record(source)  
            text = recognizer.recognize_google(audio_data)   
            print("I said:", text) 
            st.write("**You said**") 
            st.write(text) 

    except sr.UnknownValueError:  
        st.write("Sorry, I could not understand")


## Save the audio
def save_audio(audio, path):
    with wave.open(path, 'w') as f:
        f.setparams((1, 2, 16000, len(audio), "NONE", "NONE"))
        f.writeframes(struct.pack("h" * len(audio), *audio))
    st.write("Recording stopped.")
    # Calling function
    audio_to_text()


## Main function
def main():
    st.title("Audio to receipt generator")

    # Reading message from the prices.txt file
    try:
        with open("prices.txt", "r") as file:
            previous_message = file.read()
    except FileNotFoundError:
        previous_message = ""

    seconds = st.number_input("Enter duration in seconds", min_value=1, value=3, step=1)
    message = st.text_area("Enter the prices of your items.", value=previous_message)

    # Creating prices.txt file and writting message on it
    with open("prices.txt", "w") as file:
        file.write(message)

    st.write(f'You wrote {len(message)} characters.')
    start_button = st.button("Start Recording")

    recorder = PvRecorder(device_index=-1, frame_length=512)
    audio = []
    path = "audio_recording.wav"
    recording = False

    if start_button:
        recording = True
        st.write("Recording...")

    if recording:
        recorder.start()
        frame_count = 0
        while recording:
            frame = recorder.read()
            audio.extend(frame)
            frame_count += 1
            if frame_count >= (32 * seconds):
                recorder.stop()
                save_audio(audio, path)
                break

if __name__ == "__main__":
    main()
