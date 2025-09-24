# Subtitle Translator - Enhanced with Multi-API Support and Real-time Progress

## Recent Updates

### 1. Multi-API Key Support
- **OpenAI and Google Gemini Support**: The application now supports both OpenAI GPT models and Google Gemini models
- **Load Balancing**: Multiple API keys can be used for the same provider to distribute load
- **Automatic Fallback**: If one API fails, the system automatically falls back to the other available API

### 2. Enhanced key.txt Format
The application now supports multiple API key formats in the `key.txt` file:

```
# API Keys Configuration
# Format 1: With prefixes (recommended)
openai:sk-your-openai-key-here
gemini:your-gemini-api-key-here

# Format 2: Multiple keys for load balancing
openai:sk-key1-here
openai:sk-key2-here  
gemini:gemini-key1-here
gemini:gemini-key2-here

# Format 3: Direct keys (auto-detected by pattern)
sk-direct-openai-key-here
direct-gemini-key-here

# Lines starting with # are ignored
# Empty lines are ignored
```

### 3. Real-time Progress Updates in GUI
- **Line-by-line Progress**: The GUI now shows exactly which subtitle line is being translated
- **Progress Bar**: A visual progress bar shows completion percentage
- **Real-time Updates**: Progress updates happen in real-time without freezing the interface
- **Threading**: Translation runs in a separate thread to keep the GUI responsive
- **Button States**: The translate button is disabled during translation to prevent multiple simultaneous translations

### 4. Enhanced GUI Features
- **API Status Display**: Shows how many API keys are loaded for each provider
- **API Preference Selection**: Choose between "auto", "openai", or "gemini" modes
- **Enhanced Error Handling**: Better error messages and status updates
- **Load/Reload Keys**: Button to reload API keys without restarting the application

### 5. Command Line Improvements
- **API Detection**: Automatically detects and reports available APIs
- **Better Logging**: More detailed progress information in command line mode
- **Multi-API Stats**: Shows count of available keys for each provider

## File Structure Changes

### New/Modified Files:
1. **main.py** - Enhanced with multi-API support and progress callbacks
2. **app_gui.py** - Updated GUI with real-time progress and threading
3. **subtitle_translator.spec** - Updated build configuration to include Gemini support
4. **requirements.txt** - Added google-generativeai dependency
5. **key_example.txt** - Example configuration file for API keys

### Integration Details:
- **gemini_test.py functionality** has been integrated into main.py
- **Multi-threading** prevents GUI freezing during translation
- **Progress callbacks** enable real-time updates from worker thread to GUI
- **API preference system** allows users to choose their preferred translation service

## Usage Instructions

### For GUI Application:
1. Place your API keys in `key.txt` using the format shown above
2. Launch `SubtitleTranslator.exe`
3. Click "Load/Reload Keys" to load your API configuration
4. Select your preferred API (auto/openai/gemini)
5. Choose your subtitle file (.ass format)
6. Select target language
7. Click "Translate" and watch real-time progress

### For Command Line:
1. Configure `key.txt` with your API keys
2. Run the script with your subtitle file path
3. The script will automatically use available APIs with load balancing

## Technical Improvements

### Performance:
- **Load Balancing**: Multiple API keys distribute requests
- **Non-blocking GUI**: Translation doesn't freeze the interface
- **Efficient Progress Updates**: Real-time updates without performance impact

### Reliability:
- **Automatic Fallback**: If one API fails, automatically try another
- **Better Error Handling**: Detailed error messages and recovery
- **Thread Safety**: Proper synchronization between worker thread and GUI

### User Experience:
- **Visual Progress**: See exactly what's happening during translation
- **Status Information**: Always know which APIs are available
- **Responsive Interface**: GUI remains usable during long translations

## Build Information
The executable now includes:
- Google Generative AI library
- Enhanced GUI with threading support
- Multi-API key management
- Real-time progress display
- All original OpenAI functionality

The build process automatically includes all necessary dependencies and creates a single executable file that contains both OpenAI and Gemini translation capabilities with real-time progress updates.
