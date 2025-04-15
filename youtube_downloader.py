from pytube import YouTube
import subprocess
import os
import sys

def download_youtube_to_mp3(youtube_url):
    """
    Downloads audio from a YouTube video and converts it to MP3.

    Args:
        youtube_url: The URL of the YouTube video.

    Returns:
        The path to the downloaded MP3 file, or None if an error occurred.
    """
    try:
        yt = YouTube(youtube_url)
        # Sanitize title for filename
        safe_title = "".join([c for c in yt.title if c.isalnum() or c in (' ', '-')]).rstrip()
        print(f"Downloading: {safe_title}")
        
        audio_stream = yt.streams.filter(only_audio=True).first()

        if not audio_stream:
            print("No audio stream found for this video.")
            return None

        # Download the audio
        # Specify output path and filename more robustly
        download_path = "."
        out_file = audio_stream.download(output_path=download_path, filename=f"{safe_title}.{audio_stream.subtype}")
        print(f"Downloaded raw audio to: {out_file}")

        base, ext = os.path.splitext(out_file)
        # It's better to keep the original extension if possible or convert directly
        # No need to rename to .mp4 unless ffmpeg requires it, which it usually doesn't

        # Convert to MP3 using ffmpeg
        mp3_file = base + '.mp3'
        print(f"Converting {out_file} to {mp3_file}...")
        # Removed stderr=subprocess.DEVNULL to show potential errors
        process = subprocess.run(['ffmpeg', '-i', out_file, mp3_file],
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.PIPE, # Capture stderr
                               text=True)
        
        if process.returncode != 0:
            print("ffmpeg conversion failed!")
            print(f"Error: {process.stderr}")
            # Optionally keep the original file if conversion fails
            # os.remove(out_file) # Don't remove if failed
            return None
        else:
            print("Conversion successful.")
            os.remove(out_file) # remove the original audio file only on success
            print(f"Downloaded and converted to: {mp3_file}")
            return mp3_file

    except Exception as e:
        print(f"An error occurred: {e}")
        # Clean up partial download if it exists and is identifiable
        # Potentially look for files matching the pattern if `out_file` wasn't assigned
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
        mp3_path = download_youtube_to_mp3(video_url)
        if mp3_path:
            # Optional: print just the path for scripting use
            # print(mp3_path)
            pass 
    else:
        print("Usage: python youtube_downloader.py <youtube_url>")
        print("Please provide a YouTube URL as a command-line argument.")
