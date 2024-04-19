import os
import uuid

import pydub
import pyttsx3
import speech_recognition as sr

recognizer = sr.Recognizer()
microphone = sr.Microphone()
synthesizer = pyttsx3.init()

language = 'ru_RU'
# 'uk_UA'


def recognise(filename)->str:
    with sr.AudioFile(filename) as source:
        audio_text = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_text, language=language)
            return text
        except sr.UnknownValueError:
            text = "Извините я не понимаю..."
            return text
        except sr.RequestError:
            text = "К сожалению, при обработке вашего запроса произошла ошибка..."
            return text


def voice_processing(downloaded_file)->str:
    filename = str(uuid.uuid4())
    file_name_full = "./Voices/Source/" + filename + ".ogg"
    file_name_full_converted = "./Voices/Ready/" + filename + ".wav"

    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file.getvalue())

    voice = pydub.AudioSegment.from_ogg(file_name_full)
    voice.export(file_name_full_converted, format="wav")

    text = recognise(file_name_full_converted)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)
    return text
