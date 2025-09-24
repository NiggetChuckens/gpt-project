import os
import sys
import subprocess
import threading
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
        ttk.Label(main_frame, text="API Keys (key.txt):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.api_status_var = tk.StringVar(value="No keys loaded")
        api_status_label = ttk.Label(main_frame, textvariable=self.api_status_var, 
                                   foreground="red")
        api_status_label.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        ttk.Button(main_frame, text="Load/Reload Keys", 
                  command=self.load_api_keys).grid(row=1, column=2, pady=5, padx=(5, 0))
        
        # API Selection
        ttk.Label(main_frame, text="Preferred API:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.api_preference_var = tk.StringVar(value="auto")
        api_combo = ttk.Combobox(main_frame, textvariable=self.api_preference_var,
                                values=["auto", "openai", "gemini"], state="readonly")
        api_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # File selection
        ttk.Label(main_frame, text="Subtitle File:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(main_frame, textvariable=self.file_path_var, width=50)
        file_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        ttk.Button(main_frame, text="Browse", 
                  command=self.browse_file).grid(row=3, column=2, pady=5, padx=(5, 0))
        
        # Language selection
        ttk.Label(main_frame, text="Target Language:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.language_var = tk.StringVar(value="Spanish")
        language_combo = ttk.Combobox(main_frame, textvariable=self.language_var,
                                     values=["Spanish", "English", "French", "German", 
                                            "Italian", "Portuguese", "Japanese", "Korean"])
        language_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Progress section
        ttk.Label(main_frame, text="Progress:").grid(row=5, column=0, sticky=tk.W, pady=(20, 5))
        self.progress_var = tk.StringVar(value="Ready to translate")
        progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        progress_label.grid(row=5, column=1, sticky=tk.W, pady=(20, 5), padx=(5, 0))
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='determinate')
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=(20, 0))
        
        ttk.Button(button_frame, text="Translate", 
                  command=self.start_translation).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).pack(side=tk.LEFT)
        
        # Output text area
        ttk.Label(main_frame, text="Output:").grid(row=8, column=0, sticky=(tk.W, tk.N), pady=(20, 5))
        
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=8, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                       pady=(20, 0), padx=(5, 0))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.output_text = tk.Text(text_frame, height=8, width=50)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights for text area
        main_frame.rowconfigure(8, weight=1)
        
        # Translation state variables
        self.translation_in_progress = False
        
        # Load API keys if available
        self.load_api_keys()
    
    def load_api_keys(self):
        """Load API keys from key.txt file and update status"""
        try:
            import main
            main.initialize_clients()
            
            openai_count = len(main.openai_clients)
            gemini_count = len(main.gemini_clients)
            
            if openai_count > 0 or gemini_count > 0:
                status = f"✓ OpenAI: {openai_count}, Gemini: {gemini_count}"
                self.api_status_var.set(status)
                # Change color to green for success
                for widget in self.root.winfo_children():
                    self._update_status_color(widget, "green")
                self.log(f"API keys loaded successfully: {status}")
            else:
                self.api_status_var.set("✗ No valid keys found")
                # Change color to red for error
                for widget in self.root.winfo_children():
                    self._update_status_color(widget, "red")
                self.log("No valid API keys found in key.txt")
                
        except FileNotFoundError:
            self.api_status_var.set("✗ key.txt file not found")
            self.log("key.txt file not found. Please create one with your API keys.")
        except Exception as e:
            self.api_status_var.set(f"✗ Error: {str(e)[:30]}...")
            self.log(f"Error loading API keys: {e}")
    
    def _update_status_color(self, widget, color):
        """Recursively update status label color"""
        try:
            if hasattr(widget, 'cget') and widget.cget('textvariable') == str(self.api_status_var):
                widget.configure(foreground=color)
        except:
            pass
        
        for child in widget.winfo_children():
            self._update_status_color(child, color)
    
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
    
    def update_progress(self, message, current_line, total_lines):
        """Update progress bar and message from translation thread"""
        # This method will be called from the translation thread
        # We need to use after() to update GUI from main thread
        self.root.after(0, self._update_progress_safe, message, current_line, total_lines)
    
    def _update_progress_safe(self, message, current_line, total_lines):
        """Safely update progress from main thread"""
        self.progress_var.set(message)
        self.progress_bar['value'] = (current_line / total_lines) * 100
        self.log(message)
    
    def start_translation(self):
        """Start the translation process"""
        # Import the main translation functions first
        import main
        
        # Check if translation is already in progress
        if self.translation_in_progress:
            messagebox.showwarning("Translation in Progress", "A translation is already running. Please wait.")
            return
        
        # Validate inputs
        if len(main.openai_clients) == 0 and len(main.gemini_clients) == 0:
            messagebox.showerror("Error", "No API keys available. Please load valid API keys first.")
            return
        
        if not self.file_path_var.get():
            messagebox.showerror("Error", "Please select a subtitle file")
            return
        
        if not os.path.exists(self.file_path_var.get()):
            messagebox.showerror("Error", "Selected file does not exist")
            return
        
        # Start translation in a separate thread
        self.translation_in_progress = True
        self.progress_var.set("Starting translation...")
        self.progress_bar['value'] = 0
        
        # Disable the translate button during translation
        for widget in self.root.winfo_children():
            self._disable_translate_button(widget)
        
        # Get translation parameters
        file_path = self.file_path_var.get()
        language = self.language_var.get()
        api_preference = self.api_preference_var.get()
        
        # Start translation thread
        translation_thread = threading.Thread(
            target=self._translate_worker, 
            args=(file_path, language, api_preference)
        )
        translation_thread.daemon = True
        translation_thread.start()
    
    def _disable_translate_button(self, widget):
        """Recursively find and disable the translate button"""
        try:
            if hasattr(widget, 'cget') and widget.cget('text') == 'Translate':
                widget.configure(state='disabled')
        except:
            pass
        
        for child in widget.winfo_children():
            self._disable_translate_button(child)
    
    def _enable_translate_button(self, widget):
        """Recursively find and enable the translate button"""
        try:
            if hasattr(widget, 'cget') and widget.cget('text') == 'Translate':
                widget.configure(state='normal')
        except:
            pass
        
        for child in widget.winfo_children():
            self._enable_translate_button(child)
    
    def _translate_worker(self, file_path, language, api_preference):
        """Worker thread for translation"""
        try:
            # Import the main translation functions
            import main
            
            self.root.after(0, self.log, f"Starting translation to {language} using {api_preference} API...")
            self.root.after(0, self.log, f"Available: OpenAI ({len(main.openai_clients)}), Gemini ({len(main.gemini_clients)})")
            
            # Determine file type and translate
            if file_path.lower().endswith('.ass'):
                result = main.translateass(
                    file_path, 
                    lang=language, 
                    api_preference=api_preference,
                    progress_callback=self.update_progress
                )
            else:
                # For SRT files, you might want to add support
                self.root.after(0, self.log, "SRT file support not implemented yet")
                result = "SRT translation not supported in this version"
            
            # Update UI with completion
            self.root.after(0, self.log, result)
            self.root.after(0, self.log, "Translation completed!")
            self.root.after(0, self._translation_finished, True)
            
        except Exception as e:
            error_msg = f"Error during translation: {e}"
            self.root.after(0, self.log, error_msg)
            self.root.after(0, messagebox.showerror, "Translation Error", f"An error occurred: {e}")
            self.root.after(0, self._translation_finished, False)
    
    def _translation_finished(self, success):
        """Called when translation is finished"""
        self.translation_in_progress = False
        self.progress_var.set("Translation completed!" if success else "Translation failed!")
        if success:
            self.progress_bar['value'] = 100
        
        # Re-enable the translate button
        for widget in self.root.winfo_children():
            self._enable_translate_button(widget)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = SubtitleTranslatorApp()
    app.run()
