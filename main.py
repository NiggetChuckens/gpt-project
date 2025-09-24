from time import sleep
from pathlib import Path 
import os, ass, openai
import random

# Try importing Google Generative AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Google Generative AI not available. Install with: pip install google-generativeai")

# Global client variables - will be set by the GUI app or loaded from file
openai_clients = []
gemini_clients = []
current_api_keys = {'openai': [], 'gemini': []}

def initialize_clients(api_keys=None):
    """Initialize clients with provided API keys or load from file"""
    global openai_clients, gemini_clients, current_api_keys
    
    if api_keys is None:
        api_keys = load_api_keys_from_file()
    
    current_api_keys = api_keys
    openai_clients = []
    gemini_clients = []
    
    # Initialize OpenAI clients
    for key in api_keys.get('openai', []):
        try:
            client = openai.Client(api_key=key)
            openai_clients.append(client)
        except Exception as e:
            print(f"Failed to initialize OpenAI client: {e}")
    
    # Initialize Gemini clients
    if GEMINI_AVAILABLE:
        for key in api_keys.get('gemini', []):
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                gemini_clients.append({'key': key, 'model': model})
            except Exception as e:
                print(f"Failed to initialize Gemini client: {e}")

def load_api_keys_from_file():
    """Load API keys from key.txt file with multi-key support"""
    api_keys = {'openai': [], 'gemini': []}
    
    try:
        with open('key.txt', 'r') as f:
            lines = f.read().strip().split('\n')
            
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):  # Skip empty lines and comments
                continue
                
            # Detect API key type
            if line.startswith('sk-'):  # OpenAI key format
                api_keys['openai'].append(line)
            elif 'openai:' in line.lower():
                key = line.split(':', 1)[1].strip()
                api_keys['openai'].append(key)
            elif 'gemini:' in line.lower():
                key = line.split(':', 1)[1].strip()
                api_keys['gemini'].append(key)
            else:
                # Try to detect by length and format (basic heuristic)
                if len(line) > 30 and not line.startswith('sk-'):
                    api_keys['gemini'].append(line)  # Assume Gemini
                elif line.startswith('sk-'):
                    api_keys['openai'].append(line)
                    
    except FileNotFoundError:
        print("API key file not found. Will use GUI to set API keys.")
    
    return api_keys

# Try to load API keys from file for standalone usage
initialize_clients()

########################################################################
def get_random_client(api_type='openai'):
    """Get a random client for load balancing"""
    if api_type == 'openai' and openai_clients:
        return random.choice(openai_clients)
    elif api_type == 'gemini' and gemini_clients:
        return random.choice(gemini_clients)
    return None

def translate_with_openai(text: str, lang: str):
    """Translate text using OpenAI API"""
    client = get_random_client('openai')
    if client is None:
        raise Exception("No OpenAI clients available. Please provide valid API keys.")
    
    prompt = (
        "Tomas el rol de un traductor experimentado dentro de la industria del entretenimiento "
        "tu trabajo sera traducir al {} el siguiente texto de manera que mantenga la coherencia y sentido originales de la frase: "
    )
    prompt = prompt.format(lang) + text

    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "user", 
                 "content": prompt}
            ],
            temperature=0.45
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI translation error: {e}")
        raise

def translate_with_gemini(text: str, lang: str):
    """Translate text using Google Gemini API"""
    if not GEMINI_AVAILABLE:
        raise Exception("Google Generative AI library not installed.")
    
    client_info = get_random_client('gemini')
    if client_info is None:
        raise Exception("No Gemini clients available. Please provide valid API keys.")
    
    model = client_info['model']
    prompt = (
        "Tomas el rol de un traductor experimentado dentro de la industria del entretenimiento "
        "tu trabajo sera traducir al {} el siguiente texto de manera que mantenga la coherencia y sentido originales de la frase: {}"
        "solo responde con la traduccion y nada mas, no agregues comentarios adicionales ni explicaciones"
    )
    
    try:
        response = model.generate_content(prompt.format(lang, text))
        result = response.text.split('*')[0].strip()
        return result
    except Exception as e:
        print(f"Gemini translation error: {e}")
        raise

def translate(text: str, lang: str, api_preference='auto'):
    """Translate text using available APIs with fallback"""
    
    # Determine which API to use
    if api_preference == 'auto':
        # Auto-select based on availability
        if openai_clients and gemini_clients:
            api_preference = random.choice(['openai', 'gemini'])
        elif openai_clients:
            api_preference = 'openai'
        elif gemini_clients:
            api_preference = 'gemini'
        else:
            raise Exception("No API clients available. Please provide valid API keys.")
    
    # Try primary API
    try:
        if api_preference == 'openai' and openai_clients:
            return translate_with_openai(text, lang)
        elif api_preference == 'gemini' and gemini_clients:
            return translate_with_gemini(text, lang)
    except Exception as e:
        print(f"Primary API ({api_preference}) failed: {e}")
        
        # Try fallback API
        try:
            if api_preference == 'openai' and gemini_clients:
                print("Falling back to Gemini API...")
                return translate_with_gemini(text, lang)
            elif api_preference == 'gemini' and openai_clients:
                print("Falling back to OpenAI API...")
                return translate_with_openai(text, lang)
        except Exception as fallback_error:
            print(f"Fallback API also failed: {fallback_error}")
            raise Exception(f"Both APIs failed. Primary: {e}, Fallback: {fallback_error}")
    
    raise Exception(f"No suitable API available for preference: {api_preference}")

########################################################################
def translateass(filepath: str, enc: str = "utf-8-sig", lang: str = "Spanish", api_preference: str = "auto", progress_callback=None) -> str:
    """Translate an ASS subtitle file"""
    with open(Path(filepath), 'r', encoding=enc) as f:
        sub = ass.parse(f)

    translatedpath = f"{filepath.rstrip('.ass')}_translated.ass"
    total_lines = len(sub.events)
    
    with open(Path(translatedpath), 'w', encoding=enc) as f:    
        f.write('[Script Info]\n')
        f.write('[Events]\n')
        f.write('Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n')
        
        for x in range(len(sub.events)):
            current_line = x + 1
            progress_msg = f'Translating line: {current_line}/{total_lines} using {api_preference} API'
            print(progress_msg)
            
            # Call progress callback if provided (for GUI updates)
            if progress_callback:
                progress_callback(progress_msg, current_line, total_lines)
            
            subs = sub.events[x]
            translated_text = translate(subs.text, lang, api_preference)
            sub.events[x].text = translated_text + '{' + str(sub.events[x].text) + '}'
            subs = sub.events[x].dump()
            
            f.write('Dialogue: ' + subs + '\n')    
    return f'File saved successfully as: {translatedpath}'

if __name__ == "__main__":
    if not openai_clients and not gemini_clients:
        print("No API keys found. Please ensure you have a 'key.txt' file with your API keys.")
        print("Format:")
        print("openai:sk-your-openai-key-here")
        print("gemini:your-gemini-key-here")
        print("Or just put the keys directly, one per line.")
        exit(1)
    
    print(f"Available APIs: OpenAI ({len(openai_clients)} keys), Gemini ({len(gemini_clients)} keys)")
    translateass("c:\\Users\\hime\\Desktop\\fansu\\Kimizero\\[UnsyncSubs] Keiken Zumi na Kimi to, Keiken Zero na Ore ga, Otsukiai Suru Hanashi - 06.ass")