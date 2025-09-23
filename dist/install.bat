@echo off
echo ================================
echo Subtitle Translator Installer
echo ================================
echo.

echo This installer will set up the Subtitle Translator application.
echo The application will automatically install Python and required packages if needed.
echo.

pause

echo Creating application directory...
if not exist "%USERPROFILE%\SubtitleTranslator" (
    mkdir "%USERPROFILE%\SubtitleTranslator"
)

echo Copying application files...
copy "SubtitleTranslator.exe" "%USERPROFILE%\SubtitleTranslator\" >nul
copy "requirements.txt" "%USERPROFILE%\SubtitleTranslator\" >nul
copy "README.md" "%USERPROFILE%\SubtitleTranslator\" >nul
if exist "key.txt" copy "key.txt" "%USERPROFILE%\SubtitleTranslator\" >nul

echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Subtitle Translator.lnk'); $Shortcut.TargetPath = '%USERPROFILE%\SubtitleTranslator\SubtitleTranslator.exe'; $Shortcut.WorkingDirectory = '%USERPROFILE%\SubtitleTranslator'; $Shortcut.Description = 'Subtitle Translator - Translate subtitle files using OpenAI GPT'; $Shortcut.Save()"

echo.
echo Installation completed successfully!
echo.
echo The application has been installed to: %USERPROFILE%\SubtitleTranslator
echo A desktop shortcut has been created.
echo.
echo You can now run the application from the desktop shortcut or by navigating to:
echo %USERPROFILE%\SubtitleTranslator\SubtitleTranslator.exe
echo.
echo Note: On first run, the application may need to install Python and required packages.
echo This requires an internet connection and may take several minutes.
echo.
pause
