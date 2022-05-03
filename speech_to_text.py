import speech_recognition as sr

filename = "file_3.wav"

# initialize the recognizer
recog = sr.Recognizer()

# open the file
with sr.AudioFile(filename) as source:
    
    # listen for the data (load audio to memory)
    audio_data = recog.record(source)

    # recognize (convert from speech to text)
    text = recog.recognize_google(audio_data)
    print(text)