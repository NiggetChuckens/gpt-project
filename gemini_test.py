import ass
from pathlib import Path
import google.generativeai as genai

# Configure the API key
try:
    with open('key.txt', 'r') as f:
        api_key = f.read().strip()
    # Check if it's actually a Google AI API key (basic check)
    if api_key == "HERE_GOES_YOUR_OPENAI_API_KEY" or "sk-" in api_key:
        print("Error: key.txt contains an OpenAI API key, but this script needs a Google AI API key.")
        print("Please get a Google AI API key from: https://aistudio.google.com/app/apikey")
        print("Or use the openai_test.py script instead for OpenAI.")
        exit(1)
    
    genai.configure(api_key=api_key)
except FileNotFoundError:
    print("Please create a key.txt file with your Google AI API key")
    exit(1)


def translate(text: str, lang: str):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = (
            "Tomas el rol de un traductor experimentado dentro de la industria del entretenimiento "
            "tu trabajo sera traducir al {} el siguiente texto de manera que mantenga la coherencia y sentido originales de la frase: {}"
            "solo responde con la traduccion y nada mas, no agregues comentarios adicionales ni explicaciones"
        )
    response = model.generate_content(prompt.format(lang, text))    
    print(response.text.split('*')[0])
    return response.text.split('*')[0]

########################################################################
def translateass(filepath: str, enc: str = "utf-8-sig", lang: str = "Spanish") -> str:    
    """Translate an ASS subtitle file"""
    with open(Path(filepath), 'r', encoding=enc) as f:
        sub = ass.parse(f)

    translatedpath = f"{filepath.rstrip('.ass')}_translated.ass"
    with open(Path(translatedpath), 'w', encoding=enc) as f:    
        f.write('[Script Info]\n')
        f.write('[Events]\n')
        f.write('Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n')
        
        for x in range(len(sub.events)):
            subs = sub.events[x]
            
            print(sub.events[x])
            
            translated_text = translate(subs.text, lang)


            text = translated_text + "{" + str(sub.events[x].text) + "}"
            print(f'Translated line {x + 1}: {text}')

            from time import sleep
            sleep(1)

            sub.events[x].text = text
            subs = sub.events[x].dump()
            f.write('Dialogue: ' + subs + '\n')    
            
    return f'File saved successfully as: {translatedpath}'

if __name__ == "__main__":
   translateass("c:\\Users\\Administrator\\Desktop\\fansu\\Kimizero\\[UnsyncSubs] Keiken Zumi na Kimi to, Keiken Zero na Ore ga, Otsukiai Suru Hanashi - 06.ass")