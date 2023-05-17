import ass
import pysrt
import openai
from pathlib import Path

openai.api_key = input('For this script is necessary an OpenAi API Key, if you have one paste it here: ') #API key

########################################################################
#Translate text
def translate(text:str):
    prompt =(
        "You are going to be a good translator "
        "I need this text precisely in spanish trying to keep the same meaning "
        "Translate from [START] to [END]:\n[START]"
    )
    prompt += text + "\n[END]"
        
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        max_tokens=3000,
        temperature=0.4
    )
    return response.choices[0].text.strip()

########################################################################
#Translate a srt file    
def translate_srt(file_path:str):
    
    input_data = open(file_path, 'r').read()    #input file path
    subs=pysrt.from_string(input_data)          #read srt file

    for index, subtitule in enumerate(subs):    
        subtitule.text = translate(subtitule.text)  #pass the text inside the actual index on translate function
        print(subtitule)
    exit()   

########################################################################
#Transcribe an audio
def transcript_audio(audio_file:str, form:str, lan:str):
    audio_file=open(audio_file, 'rb') #audio file path
    transcript=openai.Audio.transcribe(
        file = audio_file,
        model ="whisper-1", 
        response_format=str(form),  #select output file format (srt, text)
        languaje=str(lan)   #Define languaje of the audio
        )
    return transcript

########################################################################
#Save a file        
def save_file(file_path:str, subs:str):
    with open(file_path, 'w') as f:
        f.write(subs)
        print("File saved successfully!")

########################################################################
#Translate and save srt file
def save_srt(file_path:str, translated_file_path:str):
    
    input_data = open(file_path, 'r').read()    #input file path
    subs=pysrt.from_string(input_data)          #read srt file

    for index, subtitule in enumerate(subs):    
        subtitule.text = translate(subtitule.text)  #pass the text inside the actual index on translate function
        with open(translated_file_path, 'a', encoding='utf-8') as f:    #create a file on the route we give before
            f.write(str(subtitule)+'\n')    #writes data on the file
    print('File saved successfully!')

########################################################################        
#Menu      

def option():
    option=input('This is an AI powered translator and transcriptor. \nWhich option do you want to use?\n 1. Transcriptor \n 2. Translator \n 3. Exit\nOption: ')
    if option == '1' or option == '2' or option == '3':
        return int(option)
    else:
        option()

def menu(option:int):
        
    ########################################################################
    #Transcriptor option
    if option==1:
        
        file=input('Please, enter the path of the audio file: ')
        form=input('Please, enter the format of the output file (srt, text): ')
        lan=input('Please, enter the languaje of the audio (en, es, jp): ')
        
        transcripted=transcript_audio(file,form,lan)
        
            
        try:    
            option=int(input('Do you want to save the transcript? \n 1. Yes \n 2. No\nOption: '))
        except:
            print('Please, enter a valid option')
            option=int(input('Do you want to save the transcript? \n 1. Yes \n 2. No\nOption: '))
        
        if option==1:
            file=input('Please, enter the path where you want to save the transcript (including the filename and extension itself): ')
            
            if form=='text':
                with open(file, 'w') as f:
                    trancript = transcripted.split(' ')
                    for x in transcripted:
                        f.write(x)
                        if x==' ':
                            f.write("\n")  
                    exit()
            else:
                save_file(file, transcripted)
                exit()
        else:
            print(transcripted)
            exit()
    
    ########################################################################
    #Traduction option
    if option == 2:
        option=(input('Do you want to translate a text file (t), or subtitle file (s)?\n'))
        
        ########################################################################
        #If text is selected
        if option == 't' or option =='T':
        
            file=input('Please, enter the path of the text file: ')
            file=open(file, 'r')
            text=translate(file)  
            option=input('Save translated file? (y,n)\n')
            if option =='y'or option=='Y':
                route=input('define the route of the file with the filename on it: ')
                with open(route, 'w') as f:
                    f.write(text)
                    f.close
                    print('File saved successfully!')
                    exit()
            else:    
                print(text)
                exit()
        
        ########################################################################
        #If subtitle is selected
        elif option == 's' or option == 'S':
            file=input('Please, enter the path of the subtitle file: ')
            option=input('Save translated file? (y,n)\n')
            
            if option =='y'or option=='Y':
                route=input('define the route of the file with the filename on it: ')
                save_srt(file,route)  
                exit()
            else:    
                translate_srt(file)
    
    ########################################################################
    #Exit program    
    if option==3:
        exit()
menu(option())