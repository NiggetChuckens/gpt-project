# PowerShell script to build the executable
Write-Host "Building Subtitle Translator Executable..." -ForegroundColor Green
Write-Host ""

# Check if PyInstaller is installed
try {
    python -c "import PyInstaller" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller not found"
    }
} catch {
    Write-Host "PyInstaller not found. Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install PyInstaller. Please check your Python installation." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Clean previous builds
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

# Build the executable
Write-Host "Building executable..." -ForegroundColor Yellow
pyinstaller --clean subtitle_translator.spec

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "Executable location: dist\SubtitleTranslator.exe" -ForegroundColor Cyan
Write-Host ""

# Copy additional files to dist folder
if (Test-Path "key.txt") {
    Copy-Item "key.txt" "dist\"
    Write-Host "Copied key.txt to dist folder" -ForegroundColor Gray
}
Copy-Item "requirements.txt" "dist\"
if (Test-Path "README.md") {
    Copy-Item "README.md" "dist\"
}

Write-Host "Additional files copied to dist folder." -ForegroundColor Gray
Write-Host ""
Write-Host "You can now distribute the entire 'dist' folder." -ForegroundColor Green
Read-Host "Press Enter to exit"
