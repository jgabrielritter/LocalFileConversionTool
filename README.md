# Modern File Converter

A feature-rich desktop application for converting files between various formats with a modern, intuitive interface.

## Features

- **Multi-category support:** Convert files across four main categories:
  - Images (JPG, PNG, GIF, BMP, TIFF, WebP)
  - Documents (CSV, XLSX, JSON, TXT)
  - Audio (MP3, WAV, OGG, FLAC)
  - Video (MP4, AVI, MKV, WebM)

- **Advanced options for each file type:**
  - Images: Quality control, resizing options
  - Documents: Encoding selection, header options
  - Audio/Video: Codec selection, bitrate adjustment

- **Batch processing:** Convert multiple files simultaneously

- **Custom output directory:** Select where your converted files will be saved

- **Conversion history:** Track recent conversion activities

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - tkinter
  - PIL (Pillow)
  - pandas
  - subprocess
  - threading
  - shutil
  - datetime

- For audio and video conversion:
  - FFmpeg installed and available in your system PATH

## Installation

1. Clone or download this repository
2. Install the required packages:
   ```
   pip install pillow pandas
   ```
3. Ensure FFmpeg is installed for audio/video conversion:
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - macOS: Install via Homebrew with `brew install ffmpeg`
   - Linux: Install via package manager, e.g., `sudo apt install ffmpeg`

## Usage

1. Run the application:
   ```
   python modern_file_converter.py
   ```

2. Select a conversion category (Images, Documents, Audio, or Video)

3. Click "Select Files" to choose the files you want to convert

4. Choose the output format from the dropdown menu

5. Configure any additional options:
   - For images: Adjust quality, enable/disable resizing, set dimensions
   - For documents: Set encoding, include/exclude headers
   - For audio/video: Select codec and bitrate

6. Choose an output directory or use the default

7. Click "Start Conversion" to begin the process

8. View conversion progress in the status bar and check history for completed operations

## Key Components

- **User Interface:** Built with tkinter for a clean, modern look
- **Image Processing:** Uses PIL (Pillow) for image manipulations
- **Document Handling:** Leverages pandas for spreadsheet and data conversions
- **Media Conversion:** Interfaces with FFmpeg for audio/video processing
- **Threading:** Performs conversions in the background to keep the UI responsive

## Customization

You can modify the application appearance by changing the theme colors in the `__init__` method:

```python
# Set theme colors
self.primary_color = "#2563eb"  # Blue
self.secondary_color = "#f8fafc"  # Light gray
self.success_color = "#10b981"  # Green
self.warning_color = "#f59e0b"  # Amber
self.error_color = "#ef4444"  # Red
self.text_color = "#1e293b"  # Dark slate
self.bg_color = "#ffffff"  # White
```

## Troubleshooting

- **FFmpeg errors:** Ensure FFmpeg is properly installed and added to your system PATH
- **File permission issues:** Make sure you have write access to the output directory
- **Format compatibility:** Not all conversions between formats maintain all features of the original file

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
