# YouTube Downloader

A powerful and reliable YouTube video and audio downloader with a simple command-line interface.

![YouTube Downloader Demo](https://raw.githubusercontent.com/username/youtube-downloader/main/images/demo.png)

## Features

- Download videos in highest quality MP4 format
- Extract audio in MP3 format
- Select between highest quality or medium quality (faster downloads)
- Automatic FFmpeg installation for Windows users
- Easy-to-use command-line interface
- Works around YouTube's download restrictions

## Requirements

- Python 3.6 or higher
- FFmpeg (automatic installation for Windows, manual for Mac/Linux)
- Internet connection

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/username/youtube-downloader.git
cd youtube-downloader
```

### 2. Install dependencies:

```bash
pip install yt-dlp
```

### 3. Run the downloader:

```bash
python youtube_downloader.py
```

The program will automatically check for required components (FFmpeg) and offer to install them if missing.

## Usage

1. Run the program: `python youtube_downloader.py`
2. Enter the YouTube URL when prompted
3. Select format (MP4 or MP3)
4. Choose quality (for videos)
5. Specify download location (or use default)
6. Wait for download to complete

## FFmpeg Installation

### Windows
The program will attempt to download and install FFmpeg automatically. 

### macOS
Install via Homebrew:
```bash
brew install ffmpeg
```

### Linux
Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

Fedora:
```bash
sudo dnf install ffmpeg
```

Arch Linux:
```bash
sudo pacman -S ffmpeg
```

## Troubleshooting

### Common Issues

1. **"HTTP Error 403: Forbidden"**
   - The tool is designed to work around these restrictions; try with a different video

2. **FFmpeg not found**
   - Follow the program's instructions to install FFmpeg
   - Or install manually following the instructions above

3. **Permission denied errors**
   - Try running with administrator privileges

## Legal Disclaimer

This tool is provided for educational purposes only. Please respect copyright laws and the YouTube Terms of Service. Only download videos that you have permission to download.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the core download functionality
- [FFmpeg](https://ffmpeg.org/) for audio/video processing capabilities