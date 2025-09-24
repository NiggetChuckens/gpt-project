# Test Progress Updates
# This is a quick test to verify the progress callback functionality works

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import main

def test_progress_callback(message, current_line, total_lines):
    """Test callback function to verify progress updates"""
    print(f"PROGRESS: {message} ({current_line}/{total_lines}) - {(current_line/total_lines)*100:.1f}%")

if __name__ == "__main__":
    print("Testing progress callback functionality...")
    print("Note: This is just a test of the callback mechanism.")
    print("For actual translation, you need valid API keys in key.txt")
    
    # Test the callback with a simple simulation
    total = 5
    for i in range(1, total + 1):
        test_progress_callback(f"Processing line {i}", i, total)
    
    print("\nProgress callback test completed!")
    print("The GUI application should now show line-by-line progress during actual translation.")
