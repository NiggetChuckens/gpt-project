import os
import sys
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class SubtitleTranslatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Subtitle Translator")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Check if main modules are available
        self.check_dependencies()
        
        self.setup_ui()
        
    def check_dependencies(self):
        """Check if required modules are available"""
        try:
            import ass
            import pysrt
            import openai
        except ImportError as e:
            messagebox.showerror(
                "Missing Dependencies", 
                f"Required module not found: {e}\n\n"
                "Please run the setup first to install all dependencies."
            )
            sys.exit(1)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Subtitle Translator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # API Key section
        ttk.Label(main_frame, text="OpenAI API Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.api_key_var = tk.StringVar()
        api_key_entry = ttk.Entry(main_frame, textvariable=self.api_key_var, 
                                 show="*", width=50)
        api_key_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        ttk.Button(main_frame, text="Load from key.txt", 
                  command=self.load_api_key).grid(row=1, column=2, pady=5, padx=(5, 0))
        
        # File selection
        ttk.Label(main_frame, text="Subtitle File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(main_frame, textvariable=self.file_path_var, width=50)
        file_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        ttk.Button(main_frame, text="Browse", 
                  command=self.browse_file).grid(row=2, column=2, pady=5, padx=(5, 0))
        
        # Language selection
        ttk.Label(main_frame, text="Target Language:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.language_var = tk.StringVar(value="Spanish")
        language_combo = ttk.Combobox(main_frame, textvariable=self.language_var,
                                     values=["Spanish", "English", "French", "German", 
                                            "Italian", "Portuguese", "Japanese", "Korean"])
        language_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Progress section
        ttk.Label(main_frame, text="Progress:").grid(row=4, column=0, sticky=tk.W, pady=(20, 5))
        self.progress_var = tk.StringVar(value="Ready to translate")
        progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        progress_label.grid(row=4, column=1, sticky=tk.W, pady=(20, 5), padx=(5, 0))
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=(20, 0))
        
        ttk.Button(button_frame, text="Translate", 
                  command=self.start_translation).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).pack(side=tk.LEFT)
        
        # Output text area
        ttk.Label(main_frame, text="Output:").grid(row=7, column=0, sticky=(tk.W, tk.N), pady=(20, 5))
        
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=7, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                       pady=(20, 0), padx=(5, 0))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.output_text = tk.Text(text_frame, height=8, width=50)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights for text area
        main_frame.rowconfigure(7, weight=1)
        
        # Load API key if available
        self.load_api_key()
    
    def load_api_key(self):
        """Load API key from key.txt file"""
        try:
            key_path = Path('key.txt')
            if key_path.exists():
                api_key = key_path.read_text().strip()
                self.api_key_var.set(api_key)
                self.log("API key loaded from key.txt")
            else:
                self.log("key.txt file not found")
        except Exception as e:
            self.log(f"Error loading API key: {e}")
    
    def browse_file(self):
        """Browse for subtitle file"""
        file_path = filedialog.askopenfilename(
            title="Select Subtitle File",
            filetypes=[
                ("ASS files", "*.ass"),
                ("SRT files", "*.srt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.log(f"Selected file: {file_path}")
    
    def log(self, message):
        """Log message to output text area"""
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def start_translation(self):
        """Start the translation process"""
        # Validate inputs
        if not self.api_key_var.get():
            messagebox.showerror("Error", "Please enter your OpenAI API key")
            return
        
        if not self.file_path_var.get():
            messagebox.showerror("Error", "Please select a subtitle file")
            return
        
        if not os.path.exists(self.file_path_var.get()):
            messagebox.showerror("Error", "Selected file does not exist")
            return
        
        # Start translation
        self.progress_var.set("Translating...")
        self.progress_bar.start()
        
        try:
            # Import the main translation functions
            import main
            
            # Set up OpenAI client with the provided API key
            main.initialize_client(self.api_key_var.get())
            
            # Start translation
            file_path = self.file_path_var.get()
            language = self.language_var.get()
            
            self.log(f"Starting translation to {language}...")
            
            # Determine file type and translate
            if file_path.lower().endswith('.ass'):
                result = main.translateass(file_path, lang=language)
            else:
                # For SRT files, you might want to add support
                self.log("SRT file support not implemented yet")
                result = "SRT translation not supported in this version"
            
            self.log(result)
            self.log("Translation completed!")
            
        except Exception as e:
            self.log(f"Error during translation: {e}")
            messagebox.showerror("Translation Error", f"An error occurred: {e}")
        
        finally:
            self.progress_bar.stop()
            self.progress_var.set("Ready to translate")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = SubtitleTranslatorApp()
    app.run()
