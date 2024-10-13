import os
import subprocess

# Prompt for video URL
url = input("Enter the URL of the video to download: ")

# Prompt for download path
default_path = os.path.join(os.path.expanduser("~"), "Downloads")
# default_path = r"E:\Downloads\Youtube_dl"
path = input(f"Enter the path to save the file (default: {default_path}): ")
if not path:
    path = default_path

# Prompt for file format
format_choice = input("Do you want to download the video or audio? (v/a) (default: a): ")
if format_choice.lower() == "v":
    format = "mp4"
    subprocess.run(["python", "-m", "yt_dlp", "-f", f"bestvideo[ext={format}]+bestaudio[ext={format}]/best[ext={format}]/best", "-o", os.path.join(path, "%(title)s.%(ext)s"), url])
else:
    format = "m4a"
    subprocess.run(["python", "-m", "yt_dlp", "-f", f"bestaudio[ext={format}]", "-o", os.path.join(path, "%(title)s.%(ext)s"), url])
