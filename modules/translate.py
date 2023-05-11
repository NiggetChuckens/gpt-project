import pysrt
import openai
########################################################################
#Translate text
def translate(text):
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
def translate_srt(file_path):
    
    input_data = open(file_path, 'r').read()    #input file path
    subs=pysrt.from_string(input_data)          #read srt file

    for index, subtitule in enumerate(subs):    
        subtitule.text = translate(subtitule.text)  #pass the text inside the actual index on translate function
        print(subtitule)
    exit()   