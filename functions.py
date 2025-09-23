from time import sleep
from pathlib import Path 
import os, ass, pysrt, openai

try:
    api_key = Path('key.txt').read_text().strip()
    if api_key:
        client = openai.Client(api_key=api_key)
        
except FileNotFoundError:
    print("API key file not found. Please create a 'key.txt' file with your OpenAI API key.")
    exit(1)

########################################################################
#Translate text
def translate(text:str,lang:str):
    prompt =(
        "Tomas el rol de un traductor experimentado dentro de la industria del entretenimiento "
        "tu trabajo sera traducir al {} el siguiente texto de manera que mantenga la coherencia y sentido originales de la frase: "
    )
    prompt=prompt.format(lang)+text

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role": "user", 
             "content": prompt}
        ],
        max_tokens=3000,
        temperature=0.45
    )
    return response.choices[0].text.strip()

########################################################################
#Translate a ass file 
def translateass(filepath: str, enc: str = "utf-8-sig", lang: str= "sp") -> str:
    with open(Path(filepath), 'r', encoding=enc) as f:
            sub=ass.parse(f)

    translatedpath = f"{filepath.strip('.ass')}_translated.ass"
    with open(Path(translatedpath), 'w', encoding=enc) as f:    
        f.write('[Script Info]')
        f.write('\n')
        f.write('[Events]')
        f.write('\n')
        f.write('Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text')
        f.write('\n')
        for x in range(0,len(sub.events)):
            print('Translating line:',x)
            subs=sub.events[x]
            subs=translate(subs.text, lang)
            sub.events[x].text = subs+'{'+str(sub.events[x].text)+'}'
            subs=sub.events[x].dump()
            
            f.write('Dialogue: '+subs+'\n')    
        return 'File saved successfully!'

translateass("c:\\Users\\Administrator\\Desktop\\fansu\\Kimizero\\[UnsyncSubs] Keiken Zumi na Kimi to, Keiken Zero na Ore ga, Otsukiai Suru Hanashi - 06.ass")
########################################################################
#Translate a srt file    
def translate_srt(file_path:str, lang:str):
    
    input_data = open(Path(file_path), 'r').read()    #input file path
    subs=pysrt.from_string(input_data)          #read srt file

    for index, subtitule in enumerate(subs):    
        subtitule.text = translate(subtitule.text,lang)  #pass the text inside the actual index on translate function
        print(subtitule)
    exit()   

########################################################################
#Transcribe an audio
def transcript_audio(audio_file:str, form:str, lan:str):
    audio_file=open(Path(audio_file), 'rb') #audio file path
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
    with open(Path(file_path), 'w') as f:
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
    
    input_data = open(Path(file_path), 'r').read()    #input file path
    subs=pysrt.from_string(input_data)          #read srt file

    for index, subtitule in enumerate(subs):    
        subtitule.text = translate(subtitule.text,lang)  #pass the text inside the actual index on translate function
        with open(Path(translated_file_path), 'a', encoding='utf-8') as f:    #create a file on the route we give before
            f.write(str(subtitule)+'\n')    #writes data on the file
    print('File saved successfully!')
    sleep(4)
    try:
        os.system('cls')
    except:
         os.system('clear')
