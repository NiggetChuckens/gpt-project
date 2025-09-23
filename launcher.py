import os
import sys
import subprocess
from pathlib import Path


def run_setup():
    """Run the environment setup"""
    print("Running environment setup...")
    try:
        # Run the setup script
        result = subprocess.run([sys.executable, "setup_environment.py"], 
                              cwd=os.path.dirname(__file__))
        return result.returncode == 0
    except Exception as e:
        print(f"Error running setup: {e}")
        return False


def run_app():
    """Run the main application"""
    try:
        # Check if we're running as a bundled executable
        if getattr(sys, 'frozen', False):
            # Running as exe
            app_dir = os.path.dirname(sys.executable)
        else:
            # Running as script
            app_dir = os.path.dirname(__file__)
        
        os.chdir(app_dir)
        
        # Try to import required modules
        try:
            import ass
            import pysrt
            import openai
            
            # All modules available, run the GUI app
            from app_gui import SubtitleTranslatorApp
            app = SubtitleTranslatorApp()
            app.run()
            
        except ImportError:
            print("Required modules not found. Running setup...")
            if run_setup():
                print("Setup completed. Please restart the application.")
                input("Press Enter to exit...")
            else:
                print("Setup failed. Please check your internet connection and try again.")
                input("Press Enter to exit...")
    
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    run_app()
