# YouTube Downloader with FFmpeg Setup
import os
import sys
import subprocess
import platform
import zipfile
import shutil
import tempfile
from urllib.request import urlretrieve
import time


def clear_screen():
    """Clear the terminal screen based on the OS"""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def check_ffmpeg():
    """Check if FFmpeg is installed and accessible"""
    try:
        # Try to run ffmpeg -version to check if it's installed and accessible
        result = subprocess.run(['ffmpeg', '-version'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        if result.returncode == 0:
            print("✓ FFmpeg is already installed and accessible")
            return True
    except:
        pass

    return False


def download_with_progress(url, destination):
    """Download a file with a progress bar"""

    def report_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(int(downloaded * 100 / total_size), 100)

        # Create a simple progress bar
        bar_length = 30
        filled_length = int(bar_length * percent / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)

        sys.stdout.write(f"\rDownloading: |{bar}| {percent}% Complete")
        sys.stdout.flush()

    try:
        urlretrieve(url, destination, reporthook=report_progress)
        print("\nDownload complete!")
        return True
    except Exception as e:
        print(f"\nDownload failed: {e}")
        return False


def install_ffmpeg_windows():
    """Download and install FFmpeg for Windows"""
    print("\nDownloading FFmpeg for Windows...")
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "ffmpeg.zip")

    # Download the FFmpeg zip file
    if not download_with_progress(ffmpeg_url, zip_path):
        return False

    # Extract the zip file
    print("Extracting FFmpeg...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Find the bin directory in the extracted files
        bin_dir = None
        for root, dirs, files in os.walk(temp_dir):
            if "bin" in dirs:
                bin_dir = os.path.join(root, "bin")
                break

        if not bin_dir:
            print("Error: Could not find bin directory in the extracted files")
            return False

        # Create a directory for FFmpeg in the user's profile
        ffmpeg_dir = os.path.join(os.path.expanduser("~"), "ffmpeg")
        if not os.path.exists(ffmpeg_dir):
            os.makedirs(ffmpeg_dir)

        # Copy the executable files
        for file in ["ffmpeg.exe", "ffprobe.exe"]:
            src = os.path.join(bin_dir, file)
            dst = os.path.join(ffmpeg_dir, file)
            shutil.copy2(src, dst)

        print(f"✓ FFmpeg installed to: {ffmpeg_dir}")

        # Add to PATH for this session
        os.environ["PATH"] += os.pathsep + ffmpeg_dir

        # Inform user about adding to PATH
        print(
            "\nIMPORTANT: For FFmpeg to work in future sessions, you need to add it to your PATH environment variable.")
        print(f"Add this to your PATH: {ffmpeg_dir}")
        print("\nWould you like me to add it to your PATH permanently? (y/n)")
        choice = input("> ")

        if choice.lower() == "y":
            try:
                # Use Windows SetX command to add to PATH
                subprocess.run(["setx", "PATH", f"%PATH%;{ffmpeg_dir}"], check=True)
                print("✓ FFmpeg added to your PATH. You may need to restart your command prompt.")
            except Exception as e:
                print(f"Could not add to PATH automatically: {e}")
                print("Please add it to your PATH manually.")

        return True

    except Exception as e:
        print(f"Error extracting or installing FFmpeg: {e}")
        return False
    finally:
        # Clean up the temporary directory
        try:
            shutil.rmtree(temp_dir)
        except:
            pass


def install_ffmpeg():
    """Install FFmpeg based on the platform"""
    if platform.system() == "Windows":
        return install_ffmpeg_windows()
    elif platform.system() == "Darwin":  # macOS
        print("\nOn macOS, it's recommended to install FFmpeg via Homebrew:")
        print("1. Install Homebrew from https://brew.sh/ if you don't have it")
        print("2. Run this command in terminal: brew install ffmpeg")
        return False
    else:  # Linux
        print("\nOn Linux, install FFmpeg using your package manager, for example:")
        print("Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("Fedora: sudo dnf install ffmpeg")
        print("Arch Linux: sudo pacman -S ffmpeg")
        return False


def install_ytdlp():
    """Install yt-dlp if not already installed"""
    print("Checking for yt-dlp...")
    try:
        # Try to run yt-dlp --version to check if it's installed
        result = subprocess.run(['yt-dlp', '--version'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        if result.returncode == 0:
            print(f"✓ yt-dlp is already installed (version: {result.stdout.strip()})")
            return True
    except:
        pass

    print("yt-dlp is not installed. Installing now...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'yt-dlp'], check=True)
        print("✓ yt-dlp installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing yt-dlp: {e}")
        return False


def download_video(url, output_path, is_audio_only=False, quality="best"):
    """Download YouTube video using yt-dlp"""
    # Prepare the command
    cmd = ['yt-dlp']

    if is_audio_only:
        # For audio-only downloads (MP3)
        cmd.extend([
            '-f', 'bestaudio',
            '-x', '--audio-format', 'mp3',
            '--audio-quality', '0',  # 0 is best quality
            '-o', os.path.join(output_path, '%(title)s.%(ext)s')
        ])
    else:
        # For video downloads (MP4)
        if quality == "medium":
            # Medium quality (720p if available)
            cmd.extend([
                '-f', 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
                '-o', os.path.join(output_path, '%(title)s.%(ext)s')
            ])
        else:
            # Best quality
            cmd.extend([
                '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                '-o', os.path.join(output_path, '%(title)s.%(ext)s')
            ])

    # Add the URL
    cmd.append(url)

    # Execute the command
    print("\nStarting download...")
    print("This may take a few moments depending on the video size and your internet speed.")
    print("Download progress will be shown below:\n")

    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError during download: {e}")
        return False


def main():
    clear_screen()
    print("\n===== YOUTUBE DOWNLOADER WITH FFMPEG SETUP =====")

    # Make sure yt-dlp is installed
    if not install_ytdlp():
        print("Failed to install yt-dlp. Please try installing it manually with:")
        print("pip install yt-dlp")
        input("\nPress Enter to exit...")
        return

    # Check if FFmpeg is installed
    if not check_ffmpeg():
        print("\nFFmpeg is required for video/audio processing but it's not found on your system.")
        print("Would you like to install FFmpeg now? (y/n)")
        choice = input("> ")

        if choice.lower() == "y":
            if not install_ffmpeg():
                print("\nCould not automatically install FFmpeg.")
                print("Please install FFmpeg manually, then run this program again.")
                input("\nPress Enter to exit...")
                return
        else:
            print("\nFFmpeg is required for this program to work. Exiting...")
            input("\nPress Enter to exit...")
            return

    while True:
        # Get YouTube URL
        url = input("\nEnter YouTube URL: ")

        # Choose format
        print("\nChoose download format:")
        print("1. MP4 (Video)")
        print("2. MP3 (Audio only)")
        format_choice = input("Enter your choice (1 or 2): ")

        is_audio_only = format_choice == "2"

        # Set quality for videos
        quality = "best"
        if not is_audio_only:
            print("\nChoose video quality:")
            print("1. Highest available quality")
            print("2. Medium quality (720p - faster download)")
            quality_choice = input("Enter your choice (1 or 2): ")

            quality = "medium" if quality_choice == "2" else "best"

        # Set download location
        default_path = os.path.join(os.path.expanduser("~"), "Downloads")
        print(f"\nDefault download location: {default_path}")
        custom_path = input("Press Enter to use default location or type a custom path: ")

        download_path = default_path
        if custom_path:
            download_path = custom_path

        # Create the directory if it doesn't exist
        if not os.path.exists(download_path):
            try:
                os.makedirs(download_path)
            except Exception as e:
                print(f"Error creating directory: {e}")
                print(f"Using default downloads folder instead.")
                download_path = default_path

        # Download the video/audio
        success = download_video(url, download_path, is_audio_only, quality)

        if success:
            print("\n✓ Download completed successfully!")
            print(f"Your file has been saved to: {download_path}")

        # Ask if user wants to download another
        another = input("\nDo you want to download another? (y/n): ")
        if another.lower() != 'y':
            print("\nThank you for using YouTube Downloader!")
            break

        clear_screen()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

    input("\nPress Enter to exit...")