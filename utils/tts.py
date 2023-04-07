from gtts import gTTS


def text_to_speech(text, play_sound=False, is_comment=False, comment_id=None):
    language = "en"  # the language we are going to convert in

    # passing the text value to the engine and the language
    # the slow parameter tells the engine the audio should be in high speed
    audio = gTTS(text=text, lang=language, slow=False)

    # saving the audio file
    if is_comment:
        audio.save(f"./audio_files/comment {comment_id}.mp3")
    else:
        audio.save(f"./audio_files/title.mp3")
