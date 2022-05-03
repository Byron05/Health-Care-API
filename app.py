import threading, queue
import speech_recognition as sr

# initialize the queue where all the filenames will be stored
q = queue.Queue()

# hardcoded files to be converted 
filenames = ["file_1.wav", "file_2.wav", "file_3.wav"]

# initialize the recognizer
recog = sr.Recognizer()

def worker():
    while True:
        filename = q.get()

        print(f'Working on file {filename}')

        # open the file
        with sr.AudioFile(filename) as source:
    
            # listen for the data (load audio to memory)
            audio_data = recog.record(source)

            # recognize (convert from speech to text)
            text = recog.recognize_google(audio_data)
            print(text)

        print(f'Finished {filename}')
        q.task_done()

# Turn-on the worker thread.
threading.Thread(target=worker, daemon=True).start()

# Send thirty task requests to the worker.
for file in filenames:
    q.put(file)

# Block until all tasks are done.
q.join()
print('All work completed')