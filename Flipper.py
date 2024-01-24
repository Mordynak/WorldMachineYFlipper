import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext

class WMYFlipper:
    def __init__(self, root):
        # Initialize the GUI
        self.root = root
        self.root.title("Worldmachine Y Flipper")

        # Variables for folder path, labels, and buttons
        self.folder_path = tk.StringVar()
        self.y_range_label = tk.Label(self.root, text="")
        self.info_label = tk.Label(self.root, text="")
        self.ignored_count = tk.Label(self.root, text="")
        self.status_var = tk.StringVar()
        self.scan_button = tk.Button(self.root, text="Scan and Copy", command=self.scan_and_copy)

        # Instance variables for tracking statistics
        self.num_subfolders = 0
        self.num_files = 0
        self.ignored_files_count = 0
        self.y_values = set()

        # ScrolledText widget for displaying ignored files
        self.ignored_files_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20, width=60)
        self.ignored_files_text.config(state=tk.DISABLED)  # Initially disable editing

        # Initialize GUI components
        self.create_widgets()

    def create_widgets(self):
        # GUI layout setup
        frame = tk.Frame(self.root)
        frame.pack(pady=4)

        tk.Label(frame, text="Select Folder:").pack(side="left")
        tk.Entry(frame, textvariable=self.folder_path, state="readonly", width=30).pack(side="left", padx=4)
        tk.Button(frame, text="Browse", command=self.browse_folder).pack(side="left")

        self.info_label.pack(pady=1)
        self.ignored_count.pack(pady=1)
        self.y_range_label.pack(pady=1)
        self.scan_button.pack(pady=4)

        tk.Label(self.root, textvariable=self.status_var).pack(pady=5)

        tk.Label(self.root, text="Ignored Files:").pack(pady=1)
        self.ignored_files_text.pack(pady=1)

    def browse_folder(self):
        # Allow user to browse and select a folder
        folder_selected = filedialog.askdirectory()
        self.folder_path.set(folder_selected)
        
        # Scan for Y values and update labels
        self.scan_y_values(folder_selected)
        self.info_label.config(text=f"Found {self.num_files} files and {self.num_subfolders} subfolders.")
        self.ignored_count.config(text=f"Ignored files: {self.ignored_files_count}")
        self.y_range_label.config(text=f"Max Y Value: {max(self.y_values)}")
        self.status_var.set("")  # Reset status bar

    def scan_y_values(self, folder):
        # Scan folder for Y values in filenames
        self.y_values = set()
        self.num_files = 0
        self.num_subfolders = 0
        self.ignored_files_count = 0

        for foldername, subfolders, filenames in os.walk(folder):
            self.num_subfolders += 1
            for filename in filenames:
                if re.search(r'_y\d+', filename):
                    self.num_files += 1
                else:
                    self.ignored_files_count += 1
                matches = re.findall(r'_y(\d+)', filename)
                for match in matches:
                    self.y_values.add(int(match))

    def scan_and_copy(self):
        # Scan selected folder for Y values, create a flipped copy of files, and update GUI
        source_folder = self.folder_path.get()

        if not source_folder:
            self.info_label.config(text="Please select a folder.")
            return

        # Create destination folder with "_Flipped" suffix
        destination_root = os.path.join(os.path.dirname(source_folder), f"{os.path.basename(source_folder)}_Flipped")
        os.makedirs(destination_root, exist_ok=True)

        y_values = set()
        ignored_files = []
        ignored_files_count = 0

        # Scan source folder for Y values
        for foldername, subfolders, filenames in os.walk(source_folder):
            for filename in filenames:
                matches = re.findall(r'_y(\d+)', filename)
                if not matches:
                    ignored_files_count += 1
                    ignored_files.append(os.path.join(os.path.basename(foldername), filename))
                    continue

                for match in matches:
                    y_values.add(int(match))

        # If no Y values found, display a message and return
        if not y_values:
            self.info_label.config(text="No Y values found. Files not copied.")
            return

        # Determine the maximum Y value
        max_y_value = max(y_values)
        file_count = 0

        # Iterate through source folder to copy and flip files
        for foldername, subfolders, filenames in os.walk(source_folder):
            relative_folder = os.path.relpath(foldername, source_folder)
            destination_folder = os.path.join(destination_root, relative_folder)

            os.makedirs(destination_folder, exist_ok=True)

            for filename in filenames:
                source_file_path = os.path.join(foldername, filename)
                matches = re.findall(r'_y(\d+)', filename)
                if not matches:
                    continue

                for match in matches:
                    y_value = int(match)
                    inverted_y_value = max_y_value - y_value
                    new_filename = filename.replace(f"_y{y_value:02}", f"_y{inverted_y_value:02}")
                    destination_file_path = os.path.join(destination_folder, new_filename)

                    shutil.copy(source_file_path, destination_file_path)
                    file_count += 1
                    print(f"Copied: {filename} to {new_filename}")

        # Display ignored files in the ScrolledText widget
        ignored_files_text = "\n".join(ignored_files)
        self.ignored_files_text.config(state=tk.NORMAL)
        self.ignored_files_text.delete(1.0, tk.END)
        self.ignored_files_text.insert(tk.END, ignored_files_text)
        self.ignored_files_text.config(state=tk.DISABLED)

        # Update labels and status bar
        self.info_label.config(text=f"Found {file_count} files and {self.num_subfolders} subfolders.")
        self.ignored_count.config(text=f"Ignored files: {self.ignored_files_count}")
        self.y_range_label.config(text=f"Max Y Value: {max_y_value}")
        self.status_var.set(f"Files copied to:\n{destination_root}")

if __name__ == "__main__":
    # Create and run the Tkinter application
    root = tk.Tk()
    app = WMYFlipper(root)
    root.mainloop()
