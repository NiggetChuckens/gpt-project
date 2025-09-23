@echo off
echo ================================
echo Subtitle Translator Uninstaller
echo ================================
echo.

echo This will remove the Subtitle Translator application from your computer.
echo.
set /p confirm="Are you sure you want to uninstall? (Y/N): "

if /i not "%confirm%"=="Y" (
    echo Uninstallation cancelled.
    pause
    exit /b
)

echo.
echo Removing desktop shortcut...
if exist "%USERPROFILE%\Desktop\Subtitle Translator.lnk" (
    del "%USERPROFILE%\Desktop\Subtitle Translator.lnk"
    echo Desktop shortcut removed.
) else (
    echo Desktop shortcut not found.
)

echo.
echo Removing application directory...
if exist "%USERPROFILE%\SubtitleTranslator" (
    rmdir /s /q "%USERPROFILE%\SubtitleTranslator"
    echo Application directory removed.
) else (
    echo Application directory not found.
)

echo.
echo Uninstallation completed successfully!
echo.
echo Note: This uninstaller does not remove Python or packages that were installed
echo by the application, as they may be used by other programs.
echo.
pause
