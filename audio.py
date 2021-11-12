from pydub import AudioSegment
import speech_recognition as sr
import soundfile as sf
import os


def converter(file):
    print(file)
    song = AudioSegment.from_file(file, format="ogg")
    name = file[:(len(file) - 4)] + ".flac"
    print(name)
    song.export(name, format="flac")
    return name


def speech_to_text(file):
    r = sr.Recognizer()
    harvard = sr.AudioFile(file)
    with harvard as source:
        audio = r.record(source)
        print(audio)
        return r.recognize_google(audio_data=audio, language="ru-RU")


def audioToString(file):
    return speech_to_text(converter(file))
