import tkinter as tk
import threading
import time
import html
from striprtf.striprtf import rtf_to_text

class ClipboardMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        self.last_clipboard = None
        self.monitoring_active = True

    def strip_formatting(self, text):
        # Check if the text is in RTF format
        if text.startswith("{\\rtf"):
            text = rtf_to_text(text)
        text = text.strip()  # Remove leading/trailing whitespace
        text = html.unescape(text)  # Convert HTML entities to their corresponding characters
        return text

    def check_clipboard(self):
        while self.monitoring_active:
            try:
                current_clipboard = self.root.clipboard_get()
                if current_clipboard != self.last_clipboard:
                    print("Clipboard content changed.")
                    plain_text = self.strip_formatting(current_clipboard)
                    if plain_text != current_clipboard:
                        self.update_clipboard(plain_text)
                    self.last_clipboard = plain_text
                else:
                    print("Clipboard content is the same, no change.")
            except tk.TclError:
                print("No text in clipboard or error accessing clipboard.")
            time.sleep(0.5)

    def update_clipboard(self, text):
        self.monitoring_active = False
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        print(f"Updated clipboard with: {text}")
        self.monitoring_active = True

    def run(self):
        threading.Thread(target=self.check_clipboard, daemon=True).start()
        self.root.mainloop()

if __name__ == "__main__":
    monitor = ClipboardMonitor()
    monitor.run()
