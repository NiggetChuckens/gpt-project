import openai
from pathlib import Path
from modules import save_file
from modules import translate
from modules import transcript

openai.api_key = input('For this script is necessary an OpenAi API Key, if you have one paste it here: ') #API key

########################################################################        
#Menu        
def menu():
    try:
        
        option=int(input('This is an AI powered translator and transcriptor. \nWhich option do you want to use?\n 1. Transcriptor \n 2. Translator \n 3. Exit\nOption: '))
    except:
        menu()
    
    ########################################################################
    #Transcriptor option
    if option==1:
        
        file=input('Please, enter the path of the audio file: ')
        form=input('Please, enter the format of the output file (srt, text): ')
        lan=input('Please, enter the languaje of the audio (en, es, jp): ')
        
        transcripted=transcript.transcript_audio(file,form,lan)
        
            
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
            text=translate.translate(file)  
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
                save_file.save_srt(file,route)  
                exit()
            else:    
                translate.translate_srt(file)
    
    ########################################################################
    #Exit program    
    if option==3:
        exit()
    
menu()