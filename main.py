import os 
import sys
import pysrt
import openai

openai.api_key = ''

#Transcribe an audio

audio_file=open('paht/to/file', 'rb')
transcript=openai.Audio.transcribe(
    file = audio_file,
    model ="whisper-1", 
    response_format='srt',
    languaje="jp"
    )

'''input_data = open('path/to/file', 'r').read()
subs=pysrt.from_string(input_data)

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
    print(subtitule)'''
    

print(transcript)

with open('path/to file', 'w') as file:
    file.write(transcript)
#print(translate)