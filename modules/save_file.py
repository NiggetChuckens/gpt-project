import pysrt
import openai
import translate
########################################################################
#Save a file        
def save_file(file_path, subs):
    with open(file_path, 'w') as f:
        f.write(subs)
        print("File saved successfully!")

########################################################################
#Translate and save srt file
def save_srt(file_path, translated_file_path):
    
    input_data = open(file_path, 'r').read()    #input file path
    subs=pysrt.from_string(input_data)          #read srt file

    for index, subtitule in enumerate(subs):    
        subtitule.text = translate(subtitule.text)  #pass the text inside the actual index on translate function
        with open(translated_file_path, 'a', encoding='utf-8') as f:    #create a file on the route we give before
            f.write(str(subtitule)+'\n')    #writes data on the file
    print('File saved successfully!')