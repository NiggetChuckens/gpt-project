import openai
########################################################################
#Transcribe an audio
def transcript_audio(audio_file, form, lan):
    audio_file=open(audio_file, 'rb') #audio file path
    transcript=openai.Audio.transcribe(
        file = audio_file,
        model ="whisper-1", 
        response_format=str(form),  #select output file format (srt, text)
        languaje=str(lan)   #Define languaje of the audio
        )
    return transcript