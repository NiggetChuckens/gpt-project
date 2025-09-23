# Subtitle Translator

A desktop application that translates subtitle files using OpenAI's GPT API. The application can automatically install Python and all required dependencies.

## Features

- **Automatic Setup**: Installs Python and required packages automatically
- **User-Friendly GUI**: Easy-to-use graphical interface
- **Multiple Formats**: Supports ASS subtitle files (SRT support coming soon)
- **Language Support**: Translate to multiple languages including Spanish, English, French, German, Italian, Portuguese, Japanese, and Korean
- **Standalone Executable**: Can be distributed as a single executable file

## Quick Start

### Option 1: Use Pre-built Executable

1. Download the `SubtitleTranslator.exe` file
2. Run the executable
3. If Python or required packages are missing, the app will install them automatically
4. Enter your OpenAI API key or place it in a `key.txt` file
5. Select your subtitle file and target language
6. Click "Translate"

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
   
   # Or PowerShell
   .\build_exe.ps1
   ```

## API Key Setup

You need an OpenAI API key to use this application:

1. **Get an API key**:
   - Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create a new API key
   - Copy the key

2. **Set up the API key**:
   - **Option A**: Enter it in the GUI when prompted
   - **Option B**: Create a `key.txt` file in the same directory as the executable and paste your API key there

## Usage

1. **Launch the application**
2. **Enter your OpenAI API key** (or load from key.txt)
3. **Select subtitle file** using the Browse button
4. **Choose target language** from the dropdown
5. **Click "Translate"** to start the process
6. **Wait for completion** - the translated file will be saved with "_translated" suffix

## Supported File Formats

- **ASS files** (.ass) - Full support
- **SRT files** (.srt) - Coming in future update

## System Requirements

- **Operating System**: Windows 10 or later
- **Memory**: 2GB RAM minimum, 4GB recommended
- **Storage**: 500MB free space for installation
- **Internet**: Required for initial setup and translation API calls

## Troubleshooting

### Common Issues

1. **"API key not found" error**:
   - Make sure your API key is correctly entered in the GUI
   - Or create a `key.txt` file with your API key

2. **"Module not found" error**:
   - Run the application again - it will attempt to install missing packages
   - Check your internet connection

3. **Translation fails**:
   - Verify your API key is valid and has sufficient credits
   - Check your internet connection
   - Ensure the subtitle file is not corrupted

4. **Python installation fails**:
   - Run the application as Administrator
   - Check your internet connection
   - Manually install Python from python.org

### Getting Help

If you encounter issues:
1. Check the output log in the application
2. Ensure you have a stable internet connection
3. Verify your OpenAI API key is valid
4. Try running as Administrator if installation fails

## File Structure

```
SubtitleTranslator/
│
├── launcher.py              # Main launcher script
├── app_gui.py              # GUI application
├── main.py                 # Core translation functions
├── setup_environment.py    # Python and package installer
├── requirements.txt        # Python dependencies
├── subtitle_translator.spec # PyInstaller configuration
├── build_exe.bat          # Windows build script
├── build_exe.ps1          # PowerShell build script
├── key.txt                # API key file (optional)
└── README.md              # This file
```

## Development

### Building the Executable

To build your own executable:

1. **Install PyInstaller**:
   ```
   pip install pyinstaller
   ```

2. **Run the build script**:
   ```
   # Windows Command Prompt
   build_exe.bat
   
   # PowerShell
   .\build_exe.ps1
   
   # Manual build
   pyinstaller --clean subtitle_translator.spec
   ```

3. **Find the executable**:
   - The built executable will be in the `dist/` folder
   - Distribute the entire `dist/` folder

### Customization

- **Add new languages**: Edit the language list in `app_gui.py`
- **Change translation model**: Modify the model parameter in `main.py`
- **Add file format support**: Extend the translation functions

## Original Tutorial

https://streamable.com/96gwmr

## License

This project is provided as-is for educational and personal use.

## Credits

- Uses OpenAI's GPT API for translation
- Built with Python and Tkinter
- Packaged with PyInstaller
