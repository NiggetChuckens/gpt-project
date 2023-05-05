import os 
import sys
import pysrt
import openai

openai.api_key = '' #API key


#Transcribe an audio
def transcript_audio(audio_file):
    audio_file=open(audio_file, 'rb') #audio file path
    transcript=openai.Audio.transcribe(
        file = audio_file,
        model ="whisper-1", 
        response_format='srt',  #select output file format (srt, text)
        languaje="jp"   #Define languaje of the audio
        )
    return transcript

def translate_srt(file_path):
    
    input_data = open(file_path, 'r').read()    #input file path
    subs=pysrt.from_string(input_data)          #read srt file

    #Define prompt for the translation
    prompt_base=(
        "You are going to be a good translator "
        "I need this text precisely in spanish trying to keep the same meaning "
        "Translate from [START] to [END]:\n[START]"
    )

    def translate(text):
        prompt = prompt_base
        prompt += text + "\n[END]"
        
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            max_tokens=3000,
            temperature=0
        )
        return response.choices[0].text.strip()

    for index, subtitule, text in enumerate(subs):
        subtitule.text = translate(subtitule.text)  
        print(subtitule)
    return subtitule
        
def save_file(file_path, subs):
    with open(file_path, 'w') as f:
        f.write(subs.to_srt())
        print("File saved successfully!")
        
def menu():
    try:
        option=int(input('This is an AI powered translator and transcriptor. \nWhich option do you want to use?\n 1. Transcriptor \n 2. Translator \n 3. Exit'))
    except:
        menu()
    if option==1:
        file=input('Please, enter the path of the audio file: ')
        transcript=transcript_audio(file)
        try:    
            option=int(input('Do you want to save the transcript? \n 1. Yes \n 2. No'))
        except:
            print('Please, enter a valid option')
            option=int(input('Do you want to save the transcript? \n 1. Yes \n 2. No'))
        if option==1:
            file=input('Please, enter the path where you want to save the transcript: ')
            with open(file, 'w') as f:
                f.write(transcript)
                print('File saved successfully!')
        
        'print(transcript)'
    
menu()
'''with open('path/to file', 'w') as file:
    file.write(transcript)'''

'''print(transcript_audio())'''


#print(translate)