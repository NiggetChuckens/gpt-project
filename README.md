# Subtitle Translator

A desktop application that translates subtitle files using OpenAI's GPT API and Google Gemini API. The application supports multi-API keys for load balancing and can automatically install Python and all required dependencies.

## Features

- **Multi-API Support**: Works with both OpenAI GPT and Google Gemini APIs
- **Load Balancing**: Supports multiple API keys for better performance and reliability
- **API Fallback**: Automatically switches to backup API if primary fails
- **Automatic Setup**: Installs Python and required packages automatically
- **User-Friendly GUI**: Easy-to-use graphical interface with API selection
- **Multiple Formats**: Supports ASS subtitle files (SRT support coming soon)
- **Language Support**: Translate to multiple languages including Spanish, English, French, German, Italian, Portuguese, Japanese, and Korean
- **Standalone Executable**: Can be distributed as a single executable file

## API Keys Setup

The application supports both OpenAI and Google Gemini APIs. Create a `key.txt` file in the same directory as the executable with your API keys:

### Format Options:

**Option 1 - With prefixes (recommended):**
```
openai:sk-your-openai-key-here
gemini:your-gemini-api-key-here
```

**Option 2 - Auto-detection:**
```
sk-your-openai-key-here
your-gemini-api-key-here
```

**Option 3 - Multiple keys for load balancing:**
```
openai:sk-key1-here
openai:sk-key2-here
gemini:gemini-key1-here
gemini:gemini-key2-here
```

### Getting API Keys:
- **OpenAI**: Get your API key from [OpenAI API Platform](https://platform.openai.com/api-keys)
- **Google Gemini**: Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Quick Start

### Option 1: Use Pre-built Executable

1. Download the `SubtitleTranslator.exe` file
2. Run the executable
3. If Python or required packages are missing, the app will install them automatically
4. Create a `key.txt` file with your API keys (see format above)
5. Use "Load/Reload Keys" button to load your API keys
6. Select your preferred API (auto, openai, or gemini)
7. Select your subtitle file and target language
8. Click "Translate"

### Option 2: Build from Source

1. **Prerequisites**:
   - Python 3.8 or higher
   - Git (optional)

2. **Clone or download the project**:
   ```
   git clone <repository-url>
   cd subtitle-translator
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```
   python launcher.py
   ```

5. **Build executable** (optional):
   ```
   # Windows Command Prompt
   build_exe.bat
   
   # Windows PowerShell
   .\build_exe.ps1
   
   # Manual build
   pyinstaller subtitle_translator.spec
   ```

## How It Works

The application works by:

1. **Loading API Keys**: Reads multiple API keys from `key.txt` file
2. **Load Balancing**: Randomly selects from available API keys for each translation
3. **Fallback System**: If one API fails, automatically tries the other
4. **Translation**: Sends subtitle text to the selected AI service
5. **Format Preservation**: Maintains subtitle timing and formatting
6. **Output**: Creates a new file with "_translated" suffix

## Supported File Formats

### Currently Supported:
- **.ass files** (Advanced SubStation Alpha)

### Coming Soon:
- **.srt files** (SubRip Text)

## API Preference Options

- **auto**: Automatically selects between available APIs for load balancing
- **openai**: Prefers OpenAI GPT-4 (with Gemini as fallback)
- **gemini**: Prefers Google Gemini (with OpenAI as fallback)

## Translation Models

- **OpenAI**: Uses GPT-4o-mini model for cost-effective translation
- **Google Gemini**: Uses Gemini-2.5-flash model for fast translation

## Project Structure

```
subtitle-translator/
├── launcher.py              # Main entry point and dependency installer
├── app_gui.py              # GUI application
├── main.py                 # Core translation functions with multi-API support
├── functions.py            # Legacy translation functions
├── gemini_test.py          # Original Gemini implementation (now integrated)
├── requirements.txt        # Python dependencies
├── subtitle_translator.spec # PyInstaller build configuration
├── key.txt                 # API keys (create this file)
├── key_example.txt         # Example API key format
└── build_exe.*             # Build scripts
```

## Dependencies

The application automatically installs these dependencies:
- `ass` - ASS subtitle file parsing
- `pysrt` - SRT subtitle file parsing
- `openai` - OpenAI API client
- `google-generativeai` - Google Gemini API client
- `pyinstaller` - For building executables

## Building the Executable

To build your own executable:

1. **Ensure environment is set up**:
   ```bash
   python setup_environment.py
   ```

2. **Build using batch file (Windows)**:
   ```cmd
   build_exe.bat
   ```

3. **Or build using PowerShell**:
   ```powershell
   .\build_exe.ps1
   ```

4. **Or build manually**:
   ```bash
   pyinstaller --clean subtitle_translator.spec
   ```

The executable will be created in the `dist/` folder as `SubtitleTranslator.exe`.

## Troubleshooting

### Common Issues:

1. **"No API keys found"**:
   - Ensure `key.txt` exists in the same folder as the executable
   - Check the key format (see examples above)
   - Use "Load/Reload Keys" button after creating/editing the file

2. **"API request failed"**:
   - Check your internet connection
   - Verify your API keys are valid and have sufficient credits
   - Try switching to the other API using the preference dropdown

3. **"File not found"**:
   - Ensure the subtitle file exists and is not corrupted
   - Check that the file has the correct extension (.ass)

4. **Translation quality issues**:
   - Try switching between OpenAI and Gemini APIs
   - The system preserves original text in curly braces for reference

### Getting Help:

- Check the output window in the GUI for detailed error messages
- Ensure you have the latest version of the application
- Verify your API keys have sufficient quota/credits

## License

This project is open source. Please check the repository for license information.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Additional subtitle format support
- New translation features
- Bug fixes
- UI improvements

## API Rate Limits

- **OpenAI**: Varies by plan, check your OpenAI dashboard
- **Google Gemini**: Check Google AI Studio for your limits

The application includes a 1-second delay between requests to respect rate limits.
