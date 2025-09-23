import sys
import importlib.util

def check_modules():
    """Check if all required modules can be imported"""
    required_modules = ['ass', 'pysrt', 'openai', 'tkinter']
    missing_modules = []
    
    print("Checking required modules...")
    
    for module in required_modules:
        try:
            if module == 'tkinter':
                import tkinter
                print(f"✓ {module} - Available")
            else:
                spec = importlib.util.find_spec(module)
                if spec is not None:
                    print(f"✓ {module} - Available")
                else:
                    missing_modules.append(module)
                    print(f"✗ {module} - Missing")
        except ImportError:
            missing_modules.append(module)
            print(f"✗ {module} - Missing")
    
    if missing_modules:
        print(f"\nMissing modules: {', '.join(missing_modules)}")
        print("The application will attempt to install these automatically.")
    else:
        print("\n✓ All required modules are available!")
    
    return len(missing_modules) == 0

def check_files():
    """Check if all required files are present"""
    import os
    
    required_files = [
        'launcher.py',
        'app_gui.py', 
        'main.py',
        'setup_environment.py',
        'requirements.txt'
    ]
    
    missing_files = []
    
    print("\nChecking required files...")
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} - Found")
        else:
            missing_files.append(file)
            print(f"✗ {file} - Missing")
    
    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        return False
    else:
        print("\n✓ All required files are present!")
        return True

if __name__ == "__main__":
    print("Subtitle Translator - Build Verification")
    print("=" * 40)
    
    files_ok = check_files()
    modules_ok = check_modules()
    
    print("\n" + "=" * 40)
    if files_ok and modules_ok:
        print("✓ Build verification PASSED")
        print("The application should work correctly.")
    elif files_ok:
        print("⚠ Build verification PARTIAL")
        print("Files are present but some modules are missing.")
        print("The application will attempt to install missing modules on first run.")
    else:
        print("✗ Build verification FAILED")
        print("Critical files are missing.")
    
    print("\nYou can now:")
    print("1. Run 'python launcher.py' to test the application")
    print("2. Use the built executable: dist/SubtitleTranslator.exe")
    print("3. Distribute the entire 'dist' folder to users")
    
    input("\nPress Enter to exit...")
