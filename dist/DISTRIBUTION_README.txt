# Subtitle Translator - Distribution Package

## What's Included

This package contains everything you need to run the Subtitle Translator application:

- **SubtitleTranslator.exe** - The main application executable
- **install.bat** - Optional installer that sets up the application in your user directory and creates a desktop shortcut
- **uninstall.bat** - Uninstaller to remove the application
- **requirements.txt** - List of Python packages that will be installed automatically
- **README.md** - Complete documentation and usage instructions
- **key.txt** - OpenAI API key file (if provided)

## Quick Start

### Option 1: Direct Run (Recommended for Testing)
1. Double-click `SubtitleTranslator.exe`
2. The application will start and automatically install any missing dependencies
3. Enter your OpenAI API key when prompted
4. Select a subtitle file and start translating

### Option 2: Install (Recommended for Regular Use)
1. Double-click `install.bat`
2. Follow the installation prompts
3. Use the desktop shortcut to launch the application

## System Requirements

- **Windows 10 or later**
- **Internet connection** (for initial setup and API calls)
- **2GB RAM minimum, 4GB recommended**
- **500MB free disk space**

## First Run

When you first run the application:

1. **Python Installation**: If Python is not installed, the application will download and install it automatically. This may take 5-10 minutes.

2. **Package Installation**: Required Python packages will be installed automatically. This usually takes 1-2 minutes.

3. **API Key Setup**: You'll need to provide your OpenAI API key either:
   - By entering it in the application GUI
   - By placing it in the `key.txt` file

## Getting an OpenAI API Key

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and save it securely
5. Enter it in the application or save it to `key.txt`

## Usage

1. **Launch** the application
2. **Enter API key** (first time only)
3. **Browse** for your subtitle file (.ass format)
4. **Select** target language
5. **Click Translate** and wait for completion
6. **Find** your translated file (saved with "_translated" suffix)

## Troubleshooting

- **If the application won't start**: Try running as Administrator
- **If installation fails**: Check your internet connection and try again
- **If translation fails**: Verify your API key is valid and has sufficient credits

## Support

For issues or questions, refer to the complete README.md file included in this package.

---

**Note**: This application requires an active internet connection and a valid OpenAI API key with sufficient credits for translation services.
