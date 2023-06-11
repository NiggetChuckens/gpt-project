import os
import ass
import pysrt
import openai
from time import sleep
from pathlib import Path as p

openai.api_key = input('For this script is necessary an OpenAi API Key, if you have one paste it here: ') #API key
try:
    os.system('cls')
except:
    os.system('clear')
    
########################################################################
#Translate text
def translate(text:str,lang:str):
    prompt =(
        "You are going to be a good translator "
        "I need this text precisely in {} trying to keep the same meaning "
        "Translate from [START] to [END]:\n[START]"
    )
    prompt=prompt.format(lang)
    prompt += text + "\n[END]"
        
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        max_tokens=3000,
        temperature=0.4
    )
    return response.choices[0].text.strip()

########################################################################
#Translate a ass file 
def translateass(filepath,enc,translatedpath,lang):
    with open(p(filepath), 'r', encoding=enc) as f:
            sub=ass.parse(f)
        
    with open(p(translatedpath), 'w', encoding=enc) as f:    
        f.write('[Script Info]')
        f.write('\n')
        f.write('[Events]')
        f.write('\n')
        f.write('Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text')
        f.write('\n')
        for x in range(0,len(sub.events)):
            print('Translationg line:',x)
            subs=sub.events[x]
            subs=translate(subs.text,lang)
            sub.events[x].text = subs+'{'+str(sub.events[x].text)+'}'
            subs=sub.events[x].dump()
            
            f.write('Dialogue: '+subs+'\n')    
        return 'File saved successfully!'

########################################################################
#Translate a srt file    
def translate_srt(file_path:str, lang:str):
    
    input_data = open(p(file_path), 'r').read()    #input file path
    subs=pysrt.from_string(input_data)          #read srt file

    for index, subtitule in enumerate(subs):    
        subtitule.text = translate(subtitule.text,lang)  #pass the text inside the actual index on translate function
        print(subtitule)
    exit()   

########################################################################
#Transcribe an audio
def transcript_audio(audio_file:str, form:str, lan:str):
    audio_file=open(p(audio_file), 'rb') #audio file path
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
    with open(p(file_path), 'w') as f:
        f.write(subs)
        print("File saved successfully!")
        sleep(4)
        try:
            os.system('cls')
        except:
            os.system('clear')

########################################################################
#Translate and save srt file
def save_srt(file_path:str, translated_file_path:str,lang:str):
    
    input_data = open(p(file_path), 'r').read()    #input file path
    subs=pysrt.from_string(input_data)          #read srt file

    for index, subtitule in enumerate(subs):    
        subtitule.text = translate(subtitule.text,lang)  #pass the text inside the actual index on translate function
        with open(p(translated_file_path), 'a', encoding='utf-8') as f:    #create a file on the route we give before
            f.write(str(subtitule)+'\n')    #writes data on the file
    print('File saved successfully!')
    sleep(4)
    try:
        os.system('cls')
    except:
         os.system('clear')

########################################################################        
#Menu      



def menu(option):
        
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
                sleep(4)
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
            lan=input('Please, enter the languaje for the translation: ')
            file=open(p(file), 'r')
            text=translate(file,lan)  
            option=input('Save translated file? (y,n)\n')
            if option =='y'or option=='Y':
                route=input('define the route of the file with the filename on it: ')
                with open(p(route), 'w') as f:
                    f.write(text)
                    f.close
                    print('File saved successfully!')
                    sleep(4)
                    try:
                        os.system('cls')
                    except:
                        os.system('clear')
                    exit()
            else:    
                print(text)
                exit()
        
        ########################################################################
        #If subtitle is selected
        elif option == 's' or option == 'S':
            option=input('Is a ass file(a) or srt file(s)?: ')
            
            if option == 'a' or option == 'A':
                file=input('Please, enter the path of the subtitle file: ')
                lan=input('Please, enter the languaje for the translation: ')
                savepath=input('Please, enter the path where you want to save the file: ')
                encode='utf-8-sig'
                response=translateass(file,encode,savepath,lan)
                print(response)
                sleep(4)
                try:
                    os.system('cls')
                except:
                    os.system('clear')
                exit()
                
            elif option=='s' or  option=='S':
                file=input('Please, enter the path of the subtitle file: ')
                lan=input('Please, enter the languaje for the translation: ')
                option=input('Save translated file? (y,n)\n')
                
                if option =='y'or option=='Y':
                    route=input('define the route of the file with the filename on it: ')
                    save_srt(file,route,lan)  
                    exit()
                else:    
                    translate_srt(file,lan)
    
    ########################################################################
    #Exit program    
    if option==3:
        exit()
        
def selection():
    option=input('This is an AI powered translator and transcriptor. \nWhich option do you want to use?\n 1. Transcriptor \n 2. Translator \n 3. Exit\nOption: ')
    try:
        option=int(option)
    except:
        print('Please, enter a valid option')
        selection()
    menu(option)
    

selection()
