from time import sleep
from pathlib import Path 
import os, ass, openai

# Global client variable - will be set by the GUI app
client = None

def initialize_client(api_key):
    """Initialize OpenAI client with provided API key"""
    global client
    client = openai.Client(api_key=api_key)

# Try to load API key from file for standalone usage
try:
    api_key = Path('key.txt').read_text().strip()
    if api_key:
        initialize_client(api_key)
except FileNotFoundError:
    print("API key file not found. Will use GUI to set API key.")

########################################################################
def translate(text: str, lang: str):
    """Translate text using OpenAI API"""
    if client is None:
        raise Exception("OpenAI client not initialized. Please provide API key.")
    
    prompt = (
        "Tomas el rol de un traductor experimentado dentro de la industria del entretenimiento "
        "tu trabajo sera traducir al {} el siguiente texto de manera que mantenga la coherencia y sentido originales de la frase: "
    )
    prompt = prompt.format(lang) + text

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "user", 
             "content": prompt}
        ],
        temperature=0.45
    )
    return response.choices[0].message.content.strip()

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
            print(f'Translating line: {x + 1}/{len(sub.events)}')
            subs = sub.events[x]
            translated_text = translate(subs.text, lang)
            sub.events[x].text = translated_text + '{' + str(sub.events[x].text) + '}'
            subs = sub.events[x].dump()
            
            f.write('Dialogue: ' + subs + '\n')    
    return f'File saved successfully as: {translatedpath}'

if __name__ == "__main__":
    if client is None:
        print("Please ensure you have a 'key.txt' file with your OpenAI API key.")
        exit(1)
    
    translateass("c:\\Users\\hime\\Desktop\\fansu\\Kimizero\\[UnsyncSubs] Keiken Zumi na Kimi to, Keiken Zero na Ore ga, Otsukiai Suru Hanashi - 06.ass")