import subprocess
import sys
import os
import urllib.request
import tempfile
import shutil
from pathlib import Path
import winreg


class PythonInstaller:
    def __init__(self):
        self.python_version = "3.12.0"
        self.python_url = f"https://www.python.org/ftp/python/{self.python_version}/python-{self.python_version}-amd64.exe"
        
    def is_python_installed(self):
        """Check if Python is installed and accessible"""
        try:
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            try:
                # Try to find python in PATH
                result = subprocess.run(["python", "--version"], 
                                      capture_output=True, text=True, timeout=10)
                return result.returncode == 0
            except (FileNotFoundError, subprocess.TimeoutExpired):
                return False
    
    def get_python_executable(self):
        """Get the Python executable path"""
        if sys.executable:
            return sys.executable
        
        # Try to find python in PATH
        try:
            result = subprocess.run(["where", "python"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return "python"
    
    def download_python(self, download_path):
        """Download Python installer"""
        print("Downloading Python installer...")
        try:
            urllib.request.urlretrieve(self.python_url, download_path)
            return True
        except Exception as e:
            print(f"Failed to download Python: {e}")
            return False
    
    def install_python(self):
        """Install Python if not present"""
        if self.is_python_installed():
            print("Python is already installed.")
            return True
        
        print("Python not found. Installing Python...")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            installer_path = os.path.join(temp_dir, "python_installer.exe")
            
            if not self.download_python(installer_path):
                return False
            
            try:
                # Install Python silently
                cmd = [
                    installer_path,
                    "/quiet",
                    "InstallAllUsers=1",
                    "PrependPath=1",
                    "Include_test=0"
                ]
                
                print("Installing Python... This may take a few minutes.")
                result = subprocess.run(cmd, timeout=600)  # 10 minute timeout
                
                if result.returncode == 0:
                    print("Python installed successfully!")
                    return True
                else:
                    print(f"Python installation failed with code {result.returncode}")
                    return False
                    
            except subprocess.TimeoutExpired:
                print("Python installation timed out.")
                return False
            except Exception as e:
                print(f"Error installing Python: {e}")
                return False


class PackageInstaller:
    def __init__(self, python_exe):
        self.python_exe = python_exe
        
    def install_packages(self, requirements_file=None, packages=None):
        """Install required packages"""
        if requirements_file and os.path.exists(requirements_file):
            return self.install_from_requirements(requirements_file)
        elif packages:
            return self.install_package_list(packages)
        else:
            print("No requirements file or package list provided.")
            return False
    
    def install_from_requirements(self, requirements_file):
        """Install packages from requirements.txt"""
        try:
            print(f"Installing packages from {requirements_file}...")
            cmd = [self.python_exe, "-m", "pip", "install", "-r", requirements_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("All packages installed successfully!")
                return True
            else:
                print(f"Package installation failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("Package installation timed out.")
            return False
        except Exception as e:
            print(f"Error installing packages: {e}")
            return False
    
    def install_package_list(self, packages):
        """Install a list of packages"""
        try:
            for package in packages:
                print(f"Installing {package}...")
                cmd = [self.python_exe, "-m", "pip", "install", package]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if result.returncode != 0:
                    print(f"Failed to install {package}: {result.stderr}")
                    return False
            
            print("All packages installed successfully!")
            return True
            
        except Exception as e:
            print(f"Error installing packages: {e}")
            return False


def setup_environment():
    """Main setup function"""
    print("Starting environment setup...")
    
    # Install Python if needed
    python_installer = PythonInstaller()
    if not python_installer.install_python():
        print("Failed to install Python. Exiting.")
        return False
    
    # Get Python executable
    python_exe = python_installer.get_python_executable()
    print(f"Using Python: {python_exe}")
    
    # Install packages
    package_installer = PackageInstaller(python_exe)
    
    # Try to install from requirements.txt first
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        success = package_installer.install_packages(requirements_file=requirements_file)
    else:
        # Fallback to hardcoded package list
        packages = ["ass", "pysrt", "openai"]
        success = package_installer.install_packages(packages=packages)
    
    if not success:
        print("Failed to install required packages. Exiting.")
        return False
    
    print("Environment setup completed successfully!")
    return True


if __name__ == "__main__":
    success = setup_environment()
    if success:
        print("Setup completed. You can now run the main application.")
        input("Press Enter to continue...")
    else:
        print("Setup failed. Please check the error messages above.")
        input("Press Enter to exit...")
