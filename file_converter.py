import os
import sys
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import pandas as pd
import subprocess
import threading

class FileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local File Converter")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # Set theme colors
        self.bg_color = "#f0f0f0"
        self.accent_color = "#3498db"
        self.root.configure(bg=self.bg_color)
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create title
        self.title_label = tk.Label(
            self.main_frame, 
            text="Local File Converter", 
            font=("Helvetica", 20, "bold"),
            bg=self.bg_color
        )
        self.title_label.pack(pady=(0, 20))

        # Input file frame
        self.input_frame = tk.LabelFrame(self.main_frame, text="Input Files", bg=self.bg_color)
        self.input_frame.pack(fill=tk.X, pady=10)
        
        # File selection
        self.file_frame = tk.Frame(self.input_frame, bg=self.bg_color)
        self.file_frame.pack(fill=tk.X, pady=10, padx=10)
        
        self.files_label = tk.Label(self.file_frame, text="Selected Files:", bg=self.bg_color)
        self.files_label.grid(row=0, column=0, sticky="w")
        
        self.file_count_label = tk.Label(self.file_frame, text="No files selected", bg=self.bg_color)
        self.file_count_label.grid(row=0, column=1, sticky="w")
        
        self.browse_button = tk.Button(
            self.file_frame, 
            text="Browse Files", 
            command=self.browse_files,
            bg=self.accent_color,
            fg="white",
            padx=10
        )
        self.browse_button.grid(row=0, column=2, padx=10)
        
        # Selected files display
        self.files_frame = tk.Frame(self.input_frame, bg=self.bg_color)
        self.files_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.files_listbox = tk.Listbox(self.files_frame, width=70, height=5)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.files_scrollbar = tk.Scrollbar(self.files_frame)
        self.files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox.config(yscrollcommand=self.files_scrollbar.set)
        self.files_scrollbar.config(command=self.files_listbox.yview)
        
        # Conversion options frame
        self.options_frame = tk.LabelFrame(self.main_frame, text="Conversion Options", bg=self.bg_color)
        self.options_frame.pack(fill=tk.X, pady=10)
        
        # File type selection
        self.options_inner_frame = tk.Frame(self.options_frame, bg=self.bg_color)
        self.options_inner_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.conversion_label = tk.Label(self.options_inner_frame, text="Convert to:", bg=self.bg_color)
        self.conversion_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.conversion_type = tk.StringVar()
        self.conversion_types = {
            "Images": ["jpg", "png", "gif", "bmp", "tiff", "webp"],
            "Documents": ["csv", "xlsx", "json"],
            "Audio": ["mp3", "wav", "ogg"],
            "Video": ["mp4", "avi", "mkv"]
        }
        
        self.type_combobox = ttk.Combobox(
            self.options_inner_frame, 
            textvariable=self.conversion_type,
            values=list(self.conversion_types.keys()),
            width=15
        )
        self.type_combobox.grid(row=0, column=1, padx=5)
        self.type_combobox.current(0)
        self.type_combobox.bind("<<ComboboxSelected>>", self.update_format_options)
        
        self.format_label = tk.Label(self.options_inner_frame, text="Format:", bg=self.bg_color)
        self.format_label.grid(row=0, column=2, sticky="w", padx=(10, 5))
        
        self.format_var = tk.StringVar()
        self.format_combobox = ttk.Combobox(
            self.options_inner_frame, 
            textvariable=self.format_var,
            values=self.conversion_types["Images"],
            width=10
        )
        self.format_combobox.grid(row=0, column=3, padx=5)
        self.format_combobox.current(0)
        
        # Output directory
        self.output_frame = tk.Frame(self.options_frame, bg=self.bg_color)
        self.output_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.output_label = tk.Label(self.output_frame, text="Output Directory:", bg=self.bg_color)
        self.output_label.grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        self.output_var = tk.StringVar()
        self.output_var.set(os.path.expanduser("~/Documents"))
        
        self.output_entry = tk.Entry(self.output_frame, textvariable=self.output_var, width=50)
        self.output_entry.grid(row=0, column=1, padx=5)
        
        self.output_button = tk.Button(
            self.output_frame, 
            text="Browse", 
            command=self.browse_output,
            bg=self.accent_color,
            fg="white"
        )
        self.output_button.grid(row=0, column=2, padx=5)
        
        # Conversion button
        self.convert_button = tk.Button(
            self.main_frame, 
            text="Convert Files", 
            command=self.convert_files,
            bg="#27ae60",
            fg="white",
            font=("Helvetica", 12, "bold"),
            padx=20,
            pady=10
        )
        self.convert_button.pack(pady=20)
        
        # Progress bar
        self.progress_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame, 
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            self.progress_frame, 
            text="Ready", 
            bg=self.bg_color
        )
        self.status_label.pack(pady=(5, 0))
        
        # Data members
        self.selected_files = []
        
    def browse_files(self):
        files = filedialog.askopenfilenames(
            title="Select Files to Convert",
            filetypes=(
                ("All Files", "*.*"),
                ("Images", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp"),
                ("Documents", "*.csv *.xlsx *.xls *.json"),
                ("Audio", "*.mp3 *.wav *.ogg *.flac"),
                ("Video", "*.mp4 *.avi *.mkv *.mov")
            )
        )
        
        if files:
            self.selected_files = list(files)
            self.update_file_list()
    
    def update_file_list(self):
        self.files_listbox.delete(0, tk.END)
        for file in self.selected_files:
            self.files_listbox.insert(tk.END, os.path.basename(file))
        
        file_count = len(self.selected_files)
        file_text = f"{file_count} file{'s' if file_count != 1 else ''} selected"
        self.file_count_label.config(text=file_text)
    
    def browse_output(self):
        output_dir = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_var.get()
        )
        
        if output_dir:
            self.output_var.set(output_dir)
    
    def update_format_options(self, event=None):
        category = self.conversion_type.get()
        self.format_combobox.config(values=self.conversion_types[category])
        self.format_combobox.current(0)
    
    def convert_files(self):
        if not self.selected_files:
            messagebox.showwarning("No Files Selected", "Please select files to convert.")
            return
        
        output_dir = self.output_var.get()
        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create output directory: {e}")
                return
        
        # Start conversion in a separate thread to avoid freezing the UI
        threading.Thread(target=self._convert_files_thread, daemon=True).start()
    
    def _convert_files_thread(self):
        target_format = self.format_var.get()
        file_category = self.conversion_type.get()
        output_dir = self.output_var.get()
        
        total_files = len(self.selected_files)
        self.status_label.config(text="Converting...")
        
        success_count = 0
        
        for i, file_path in enumerate(self.selected_files):
            try:
                file_name = os.path.basename(file_path)
                base_name = os.path.splitext(file_name)[0]
                output_file = os.path.join(output_dir, f"{base_name}.{target_format}")
                
                # Update progress
                progress_value = (i / total_files) * 100
                self.progress_var.set(progress_value)
                self.root.update_idletasks()
                
                if file_category == "Images":
                    self._convert_image(file_path, output_file, target_format)
                elif file_category == "Documents":
                    self._convert_document(file_path, output_file, target_format)
                elif file_category == "Audio":
                    self._convert_audio(file_path, output_file, target_format)
                elif file_category == "Video":
                    self._convert_video(file_path, output_file, target_format)
                
                success_count += 1
                
            except Exception as e:
                print(f"Error converting {file_path}: {e}")
                
        # Complete progress bar
        self.progress_var.set(100)
        self.status_label.config(text=f"Conversion complete: {success_count}/{total_files} successful")
        
        if success_count > 0:
            messagebox.showinfo("Conversion Complete", 
                f"Successfully converted {success_count} out of {total_files} files.\n"
                f"Files saved to: {output_dir}")
    
    def _convert_image(self, input_file, output_file, format):
        img = Image.open(input_file)
        if format.lower() == 'jpg':
            # Convert to RGB for JPG (handles RGBA images)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
        img.save(output_file, format=format.upper())
    
    def _convert_document(self, input_file, output_file, format):
        input_ext = os.path.splitext(input_file)[1].lower()
        
        if input_ext == '.csv':
            data = pd.read_csv(input_file)
        elif input_ext in ['.xlsx', '.xls']:
            data = pd.read_excel(input_file)
        elif input_ext == '.json':
            data = pd.read_json(input_file)
        else:
            raise ValueError(f"Unsupported input format: {input_ext}")
        
        if format == 'csv':
            data.to_csv(output_file, index=False)
        elif format == 'xlsx':
            data.to_excel(output_file, index=False)
        elif format == 'json':
            data.to_json(output_file, orient='records')
        else:
            raise ValueError(f"Unsupported output format: {format}")
    
    def _convert_audio(self, input_file, output_file, format):
        # Using FFmpeg for audio conversion
        try:
            subprocess.run([
                'ffmpeg', '-i', input_file, output_file
            ], check=True, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            messagebox.showwarning("FFmpeg Required", 
                "Audio conversion requires FFmpeg to be installed and in your PATH.")
            raise
    
    def _convert_video(self, input_file, output_file, format):
        # Using FFmpeg for video conversion
        try:
            subprocess.run([
                'ffmpeg', '-i', input_file, output_file
            ], check=True, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            messagebox.showwarning("FFmpeg Required", 
                "Video conversion requires FFmpeg to be installed and in your PATH.")
            raise

def main():
    root = tk.Tk()
    app = FileConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()