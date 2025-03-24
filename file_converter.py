import os
import sys
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
import subprocess
import threading
import shutil
from datetime import datetime

class ModernFileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern File Converter")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        # Set theme colors
        self.primary_color = "#2563eb"  # Blue
        self.secondary_color = "#f8fafc"  # Light gray
        self.success_color = "#10b981"  # Green
        self.warning_color = "#f59e0b"  # Amber
        self.error_color = "#ef4444"  # Red
        self.text_color = "#1e293b"  # Dark slate
        self.bg_color = "#ffffff"  # White
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color)
        self.style.configure("TButton", background=self.primary_color)
        self.style.configure("Success.TButton", background=self.success_color)
        self.style.configure("Primary.TButton", background=self.primary_color)
        
        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create header with logo
        self.header_frame = ttk.Frame(self.main_container)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo and title
        self.title_frame = ttk.Frame(self.header_frame)
        self.title_frame.pack(side=tk.LEFT)
        
        # Create a simple logo (a colored square with text as a placeholder)
        self.logo_canvas = tk.Canvas(self.title_frame, width=50, height=50, bg=self.primary_color, highlightthickness=0)
        self.logo_canvas.pack(side=tk.LEFT, padx=(0, 15))
        self.logo_canvas.create_text(25, 25, text="FC", fill="white", font=("Helvetica", 20, "bold"))
        
        # Title and description
        self.title_label = ttk.Label(
            self.title_frame, 
            text="Modern File Converter", 
            font=("Helvetica", 24, "bold"),
            foreground=self.primary_color
        )
        self.title_label.pack(anchor="w")
        
        self.subtitle_label = ttk.Label(
            self.title_frame, 
            text="Convert files between various formats with ease",
            font=("Helvetica", 12)
        )
        self.subtitle_label.pack(anchor="w")
        
        # Create tab control for different conversion categories
        self.tab_control = ttk.Notebook(self.main_container)
        self.tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs for different conversion types
        self.tabs = {}
        for category in ["Images", "Documents", "Audio", "Video"]:
            self.tabs[category] = ttk.Frame(self.tab_control)
            self.tab_control.add(self.tabs[category], text=category)
        
        # Tab content creation
        for category, tab in self.tabs.items():
            self.create_tab_content(tab, category)
        
        # Bottom status area
        self.status_frame = ttk.Frame(self.main_container)
        self.status_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text="Ready", 
            font=("Helvetica", 10)
        )
        self.status_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.status_frame, 
            variable=self.progress_var,
            length=200,
            mode="determinate",
            maximum=100
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Recent conversions
        self.recent_conversions = []
        
        # Bind tab selection event
        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
    def create_tab_content(self, tab, category):
        # Create a frame for the content
        content_frame = ttk.Frame(tab)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - file selection
        left_frame = ttk.LabelFrame(content_frame, text="Input Files")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # File selection buttons
        file_buttons_frame = ttk.Frame(left_frame)
        file_buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        browse_button = ttk.Button(
            file_buttons_frame, 
            text="Select Files", 
            command=lambda: self.browse_files(category),
            style="Primary.TButton"
        )
        browse_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(
            file_buttons_frame, 
            text="Clear All", 
            command=lambda: self.clear_files(category)
        )
        clear_button.pack(side=tk.LEFT)
        
        # File count label
        file_count_frame = ttk.Frame(left_frame)
        file_count_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        file_count_label = ttk.Label(
            file_count_frame, 
            text="No files selected", 
            font=("Helvetica", 10, "italic")
        )
        file_count_label.pack(anchor="w")
        
        # Files listbox with scrollbar
        files_frame = ttk.Frame(left_frame)
        files_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        files_listbox = tk.Listbox(
            files_frame, 
            selectbackground=self.primary_color,
            activestyle="none",
            font=("Helvetica", 10)
        )
        files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        files_scrollbar = ttk.Scrollbar(files_frame)
        files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        files_listbox.config(yscrollcommand=files_scrollbar.set)
        files_scrollbar.config(command=files_listbox.yview)
        
        # Right side - conversion options
        right_frame = ttk.LabelFrame(content_frame, text="Conversion Options")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Format selection
        format_frame = ttk.Frame(right_frame)
        format_frame.pack(fill=tk.X, padx=10, pady=10)
        
        format_label = ttk.Label(format_frame, text="Output Format:")
        format_label.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)
        
        format_var = tk.StringVar()
        format_options = self.get_format_options(category)
        
        format_combobox = ttk.Combobox(
            format_frame, 
            textvariable=format_var,
            values=format_options,
            width=10,
            state="readonly"
        )
        format_combobox.grid(row=0, column=1, sticky="w", padx=5, pady=10)
        if format_options:
            format_combobox.current(0)
        
        # Advanced options (placeholder)
        advanced_frame = ttk.LabelFrame(right_frame, text="Advanced Options")
        advanced_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add placeholder for future advanced options per category
        if category == "Images":
            # Quality slider for images
            quality_frame = ttk.Frame(advanced_frame)
            quality_frame.pack(fill=tk.X, padx=10, pady=10)
            
            quality_label = ttk.Label(quality_frame, text="Quality:")
            quality_label.grid(row=0, column=0, sticky="w", pady=10)
            
            quality_var = tk.IntVar(value=85)
            quality_scale = ttk.Scale(
                quality_frame, 
                from_=1, 
                to=100, 
                orient="horizontal",
                variable=quality_var,
                length=200
            )
            quality_scale.grid(row=0, column=1, padx=(10, 5), sticky="ew")
            
            quality_value = ttk.Label(quality_frame, text="85%", width=5)
            quality_value.grid(row=0, column=2, sticky="w")
            
            # Update label when slider changes
            def update_quality_label(event):
                quality_value.config(text=f"{quality_var.get()}%")
            
            quality_scale.bind("<Motion>", update_quality_label)
            
            # Resize options
            resize_frame = ttk.Frame(advanced_frame)
            resize_frame.pack(fill=tk.X, padx=10, pady=10)
            
            resize_check_var = tk.BooleanVar(value=False)
            resize_check = ttk.Checkbutton(
                resize_frame, 
                text="Resize image", 
                variable=resize_check_var
            )
            resize_check.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 5))
            
            width_label = ttk.Label(resize_frame, text="Width:")
            width_label.grid(row=1, column=0, sticky="w", pady=5)
            
            width_var = tk.StringVar(value="800")
            width_entry = ttk.Entry(resize_frame, textvariable=width_var, width=8)
            width_entry.grid(row=1, column=1, padx=5, sticky="w")
            
            height_label = ttk.Label(resize_frame, text="Height:")
            height_label.grid(row=2, column=0, sticky="w", pady=5)
            
            height_var = tk.StringVar(value="600")
            height_entry = ttk.Entry(resize_frame, textvariable=height_var, width=8)
            height_entry.grid(row=2, column=1, padx=5, sticky="w")
        
        elif category == "Documents":
            # Encoding options for documents
            encoding_frame = ttk.Frame(advanced_frame)
            encoding_frame.pack(fill=tk.X, padx=10, pady=10)
            
            encoding_label = ttk.Label(encoding_frame, text="Encoding:")
            encoding_label.grid(row=0, column=0, sticky="w", pady=10)
            
            encoding_var = tk.StringVar(value="utf-8")
            encoding_combobox = ttk.Combobox(
                encoding_frame, 
                textvariable=encoding_var,
                values=["utf-8", "ascii", "latin-1", "utf-16"],
                width=10,
                state="readonly"
            )
            encoding_combobox.grid(row=0, column=1, padx=5, sticky="w")
            encoding_combobox.current(0)
            
            # Header options for CSV
            header_frame = ttk.Frame(advanced_frame)
            header_frame.pack(fill=tk.X, padx=10, pady=10)
            
            header_var = tk.BooleanVar(value=True)
            header_check = ttk.Checkbutton(
                header_frame, 
                text="Include headers", 
                variable=header_var
            )
            header_check.pack(anchor="w")
        
        elif category in ["Audio", "Video"]:
            # Audio/video options
            codec_frame = ttk.Frame(advanced_frame)
            codec_frame.pack(fill=tk.X, padx=10, pady=10)
            
            codec_label = ttk.Label(codec_frame, text="Codec:")
            codec_label.grid(row=0, column=0, sticky="w", pady=10)
            
            codec_options = ["default"]
            if category == "Audio":
                codec_options += ["mp3", "aac", "ogg"]
            else:  # Video
                codec_options += ["h264", "h265", "vp9"]
                
            codec_var = tk.StringVar(value="default")
            codec_combobox = ttk.Combobox(
                codec_frame, 
                textvariable=codec_var,
                values=codec_options,
                width=10,
                state="readonly"
            )
            codec_combobox.grid(row=0, column=1, padx=5, sticky="w")
            codec_combobox.current(0)
            
            # Bitrate options
            bitrate_frame = ttk.Frame(advanced_frame)
            bitrate_frame.pack(fill=tk.X, padx=10, pady=10)
            
            bitrate_label = ttk.Label(bitrate_frame, text="Bitrate:")
            bitrate_label.grid(row=0, column=0, sticky="w", pady=10)
            
            if category == "Audio":
                bitrate_options = ["128k", "192k", "256k", "320k"]
            else:  # Video
                bitrate_options = ["1M", "2M", "5M", "10M"]
                
            bitrate_var = tk.StringVar(value=bitrate_options[1])
            bitrate_combobox = ttk.Combobox(
                bitrate_frame, 
                textvariable=bitrate_var,
                values=bitrate_options,
                width=10,
                state="readonly"
            )
            bitrate_combobox.grid(row=0, column=1, padx=5, sticky="w")
            bitrate_combobox.current(1)
        
        # Output directory selection
        output_frame = ttk.Frame(right_frame)
        output_frame.pack(fill=tk.X, padx=10, pady=10)
        
        output_label = ttk.Label(output_frame, text="Output Directory:")
        output_label.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=10)
        
        output_var = tk.StringVar()
        output_var.set(os.path.expanduser("~/Documents"))
        
        output_entry = ttk.Entry(output_frame, textvariable=output_var, width=30)
        output_entry.grid(row=0, column=1, padx=5, pady=10)
        
        output_button = ttk.Button(
            output_frame, 
            text="Browse", 
            command=lambda: self.browse_output(output_var)
        )
        output_button.grid(row=0, column=2, padx=5, pady=10)
        
        # Start conversion button
        convert_button = ttk.Button(
            right_frame, 
            text="Start Conversion", 
            command=lambda: self.convert_files(
                category,
                files_listbox,
                format_var.get(),
                output_var.get(),
                quality_var.get() if category == "Images" else None,
                resize_check_var.get() if category == "Images" else None,
                (width_var.get(), height_var.get()) if category == "Images" else None,
                encoding_var.get() if category == "Documents" else None,
                header_var.get() if category == "Documents" else None,
                codec_var.get() if category in ["Audio", "Video"] else None,
                bitrate_var.get() if category in ["Audio", "Video"] else None
            ),
            style="Success.TButton"
        )
        convert_button.pack(fill=tk.X, padx=10, pady=20)
        
        # Recent conversions section
        history_frame = ttk.LabelFrame(right_frame, text="Recent Conversions")
        history_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        history_listbox = tk.Listbox(
            history_frame, 
            height=4,
            font=("Helvetica", 9)
        )
        history_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Store references to widgets we need to access later
        setattr(self, f"{category.lower()}_files_listbox", files_listbox)
        setattr(self, f"{category.lower()}_file_count_label", file_count_label)
        setattr(self, f"{category.lower()}_history_listbox", history_listbox)
        setattr(self, f"{category.lower()}_format_var", format_var)
        setattr(self, f"{category.lower()}_output_var", output_var)
        
        # Store selected files for this category
        setattr(self, f"{category.lower()}_files", [])
    
    def get_format_options(self, category):
        formats = {
            "Images": ["jpg", "png", "gif", "bmp", "tiff", "webp"],
            "Documents": ["csv", "xlsx", "json", "txt"],
            "Audio": ["mp3", "wav", "ogg", "flac"],
            "Video": ["mp4", "avi", "mkv", "webm"]
        }
        return formats.get(category, [])
    
    def browse_files(self, category):
        filetypes = self.get_filetypes(category)
        
        files = filedialog.askopenfilenames(
            title=f"Select {category} Files to Convert",
            filetypes=filetypes
        )
        
        if files:
            current_files = getattr(self, f"{category.lower()}_files")
            current_files.extend(files)
            self.update_file_list(category)
    
    def get_filetypes(self, category):
        if category == "Images":
            return (
                ("All Images", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("GIF", "*.gif"),
                ("BMP", "*.bmp"),
                ("TIFF", "*.tiff"),
                ("WebP", "*.webp"),
                ("All Files", "*.*")
            )
        elif category == "Documents":
            return (
                ("All Documents", "*.csv *.xlsx *.xls *.json *.txt"),
                ("CSV", "*.csv"),
                ("Excel", "*.xlsx *.xls"),
                ("JSON", "*.json"),
                ("Text", "*.txt"),
                ("All Files", "*.*")
            )
        elif category == "Audio":
            return (
                ("All Audio", "*.mp3 *.wav *.ogg *.flac"),
                ("MP3", "*.mp3"),
                ("WAV", "*.wav"),
                ("OGG", "*.ogg"),
                ("FLAC", "*.flac"),
                ("All Files", "*.*")
            )
        elif category == "Video":
            return (
                ("All Video", "*.mp4 *.avi *.mkv *.mov *.webm"),
                ("MP4", "*.mp4"),
                ("AVI", "*.avi"),
                ("MKV", "*.mkv"),
                ("MOV", "*.mov"),
                ("WebM", "*.webm"),
                ("All Files", "*.*")
            )
        else:
            return (("All Files", "*.*"),)
    
    def update_file_list(self, category):
        files = getattr(self, f"{category.lower()}_files")
        listbox = getattr(self, f"{category.lower()}_files_listbox")
        count_label = getattr(self, f"{category.lower()}_file_count_label")
        
        # Clear and repopulate the listbox
        listbox.delete(0, tk.END)
        for file in files:
            listbox.insert(tk.END, os.path.basename(file))
        
        # Update count label
        file_count = len(files)
        if file_count == 0:
            count_label.config(text="No files selected")
        else:
            count_label.config(text=f"{file_count} file{'s' if file_count != 1 else ''} selected")
    
    def clear_files(self, category):
        setattr(self, f"{category.lower()}_files", [])
        self.update_file_list(category)
    
    def browse_output(self, output_var):
        output_dir = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=output_var.get()
        )
        
        if output_dir:
            output_var.set(output_dir)
    
    def on_tab_change(self, event):
        # Get the current tab name
        current_tab = self.tab_control.tab(self.tab_control.select(), "text")
        self.status_label.config(text=f"Ready for {current_tab} conversion")
    
    def convert_files(self, category, files_listbox, format, output_dir, 
                     quality=None, resize=None, dimensions=None, 
                     encoding=None, headers=None, codec=None, bitrate=None):
        files = getattr(self, f"{category.lower()}_files")
        
        if not files:
            messagebox.showwarning("No Files Selected", f"Please select {category.lower()} to convert.")
            return
        
        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create output directory: {e}")
                return
        
        # Start conversion in a separate thread
        threading.Thread(
            target=self._convert_files_thread,
            args=(category, files, format, output_dir, quality, resize, dimensions, 
                  encoding, headers, codec, bitrate),
            daemon=True
        ).start()
    
    def _convert_files_thread(self, category, files, format, output_dir, 
                             quality, resize, dimensions, encoding, headers, codec, bitrate):
        self.status_label.config(text=f"Converting {category.lower()}...")
        self.progress_var.set(0)
        
        total_files = len(files)
        success_count = 0
        history_listbox = getattr(self, f"{category.lower()}_history_listbox")
        
        # Create timestamp for this batch
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for i, file_path in enumerate(files):
            try:
                file_name = os.path.basename(file_path)
                base_name = os.path.splitext(file_name)[0]
                output_file = os.path.join(output_dir, f"{base_name}.{format}")
                
                # Update progress
                progress_value = (i / total_files) * 100
                self.progress_var.set(progress_value)
                self.root.update_idletasks()
                
                if category == "Images":
                    self._convert_image(file_path, output_file, format, quality, resize, dimensions)
                elif category == "Documents":
                    self._convert_document(file_path, output_file, format, encoding, headers)
                elif category == "Audio":
                    self._convert_audio(file_path, output_file, format, codec, bitrate)
                elif category == "Video":
                    self._convert_video(file_path, output_file, format, codec, bitrate)
                
                success_count += 1
                
            except Exception as e:
                print(f"Error converting {file_path}: {e}")
        
        # Complete progress bar
        self.progress_var.set(100)
        self.status_label.config(text=f"Conversion complete: {success_count}/{total_files} successful")
        
        # Add to recent conversions history
        history_entry = f"{timestamp}: Converted {success_count} {category.lower()} to {format}"
        self.recent_conversions.append(history_entry)
        
        # Update history listbox in the GUI thread
        self.root.after(0, lambda: self.update_history(category, history_entry))
        
        if success_count > 0:
            messagebox.showinfo("Conversion Complete", 
                f"Successfully converted {success_count} out of {total_files} files.\n"
                f"Files saved to: {output_dir}")
    
    def update_history(self, category, entry):
        history_listbox = getattr(self, f"{category.lower()}_history_listbox")
        history_listbox.insert(0, entry)  # Add to top
        
        # Keep only the most recent 10 entries
        if history_listbox.size() > 10:
            history_listbox.delete(10, tk.END)
    
    def _convert_image(self, input_file, output_file, format, quality, resize, dimensions):
        img = Image.open(input_file)
        
        # Apply resize if needed
        if resize and dimensions:
            try:
                width, height = int(dimensions[0]), int(dimensions[1])
                img = img.resize((width, height), Image.LANCZOS)
            except (ValueError, TypeError):
                pass  # Skip if dimensions are invalid
        
        # Handle special cases for different formats
        if format.lower() == 'jpg':
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(output_file, format='JPEG', quality=quality)
        elif format.lower() == 'png':
            img.save(output_file, format='PNG', optimize=True)
        elif format.lower() == 'webp':
            img.save(output_file, format='WEBP', quality=quality)
        else:
            img.save(output_file, format=format.upper())
    
    def _convert_document(self, input_file, output_file, format, encoding, headers):
        input_ext = os.path.splitext(input_file)[1].lower()
        
        if input_ext == '.csv':
            data = pd.read_csv(input_file, encoding=encoding or 'utf-8')
        elif input_ext in ['.xlsx', '.xls']:
            data = pd.read_excel(input_file)
        elif input_ext == '.json':
            data = pd.read_json(input_file, encoding=encoding or 'utf-8')
        elif input_ext == '.txt':
            # For simple text files, just copy them
            with open(input_file, 'r', encoding=encoding or 'utf-8') as src:
                content = src.read()
            
            if format == 'csv':
                # Simple conversion: split by newlines and commas
                rows = content.strip().split('\n')
                data = pd.DataFrame([row.split(',') for row in rows])
            else:
                shutil.copy2(input_file, output_file)
                return
        else:
            raise ValueError(f"Unsupported input format: {input_ext}")
        
        if format == 'csv':
            data.to_csv(output_file, index=False, header=headers)
        elif format == 'xlsx':
            data.to_excel(output_file, index=False, header=headers)
        elif format == 'json':
            data.to_json(output_file, orient='records', force_ascii=False)
        elif format == 'txt':
            # Simple conversion for text
            with open(output_file, 'w', encoding=encoding or 'utf-8') as out:
                out.write(data.to_string(index=False, header=headers))
        else:
            raise ValueError(f"Unsupported output format: {format}")
    
    def _convert_audio(self, input_file, output_file, format, codec, bitrate):
        codec_param = []
        if codec and codec != "default":
            codec_param = ['-acodec', codec]
        
        bitrate_param = []
        if bitrate:
            bitrate_param = ['-b:a', bitrate]
        
        try:
            command = ['ffmpeg', '-i', input_file]
            command.extend(codec_param)
            command.extend(bitrate_param)
            command.append(output_file)
            
            subprocess.run(command, check=True, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            messagebox.showwarning("FFmpeg Required", 
                "Audio conversion requires FFmpeg to be installed and in your PATH.")
            raise
    
    def _convert_video(self, input_file, output_file, format, codec, bitrate):
        codec_param = []
        if codec and codec != "default":
            codec_param = ['-vcodec', codec]
        
        bitrate_param = []
        if bitrate:
            bitrate_param = ['-b:v', bitrate]
        
        try:
            command = ['ffmpeg', '-i', input_file]
            command.extend(codec_param)
            command.extend(bitrate_param)
            command.append(output_file)
            
            subprocess.run(command, check=True, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            messagebox.showwarning("FFmpeg Required", 
                "Video conversion requires FFmpeg to be installed and in your PATH.")
            raise

def main():
    root = tk.Tk()
    app = ModernFileConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()