@echo off
echo Building Subtitle Translator Executable...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller. Please check your Python installation.
        pause
        exit /b 1
    )
)

REM Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM Build the executable
echo Building executable...
pyinstaller --clean subtitle_translator.spec

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo Executable location: dist\SubtitleTranslator.exe
echo.

REM Copy additional files to dist folder
if exist "key.txt" copy "key.txt" "dist\"
copy "requirements.txt" "dist\"
copy "README.md" "dist\" 2>nul

echo Additional files copied to dist folder.
echo.
echo You can now distribute the entire 'dist' folder.
pause
