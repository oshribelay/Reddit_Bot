from gtts import gTTS
from playsound import playsound


def text_to_speech(text, play_sound=False):
    language = "en"  # the language we are going to convert in

    # passing the text value to the engine and the language
    # the slow parameter tells the engine the audio should be in high speed
    audio = gTTS(text=text, lang=language, slow=False)

    # saving the audio file
    audio.save("../audio_files/audio.mp3")

    # playing the audio file based on the play_sound parameter
    if play_sound:
        playsound("../audio_files/audio.mp3")
    else:
        pass
