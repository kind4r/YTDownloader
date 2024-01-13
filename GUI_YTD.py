import os
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk

def install_yt_dlp():
    try:
        # Check if yt-dlp is installed
        subprocess.run(["python", "-m", "yt_dlp", "--version"], check=True)
        print("yt-dlp is already installed.")
    except subprocess.CalledProcessError:
        # yt-dlp is not installed, so install it
        subprocess.run(["python", "-m", "pip", "install", "yt-dlp"])
        print("yt-dlp has been installed.")

# Call the function to check and install yt-dlp if necessary
install_yt_dlp()

def install_ffmpeg():
    try:
        # Check if ffmpeg is installed
        subprocess.run(["python", "-m", "ffmpeg", "-version"], check=True)
        print("ffmpeg is already installed.")
    except subprocess.CalledProcessError:
        # ffmpeg is not installed, so install it
        subprocess.run(["python", "-m", "pip", "install", "ffmpeg"])
        print("ffmpeg has been installed.")

# Call the function to check and install ffmpeg if necessary
install_ffmpeg()

def download_video():
    # Reset progress bar and result label
    progress_bar["mode"] = "determinate"
    progress_bar["value"] = 0
    result_label.config(text="                                                                                        ")

    url = url_entry.get()
    path = path_entry.get() or default_path
    format_choice = format_var.get()

    if format_choice == "Video":
        format = "mp4"
        cmd = ["python", "-m", "yt_dlp", "-f", f"bestvideo[ext={format}]+bestaudio[ext={format}]/best[ext={format}]/best", "-o", os.path.join(path, "%(title)s.%(ext)s"), url]
    else:
        format = "m4a"
        cmd = ["python", "-m", "yt_dlp", "-f", f"bestaudio[ext={format}]", "-o", os.path.join(path, "%(title)s.%(ext)s"), url]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while process.poll() is None:
        root.update_idletasks()
        progress = process.stdout.readline().decode("utf-8")
        if "Downloading video" in progress or "Downloading audio" in progress:
            try:
                percentage = int(progress.split()[1][:-1])
                progress_bar["value"] = percentage
            except ValueError:
                pass

    progress_bar["value"] = 100

    result_label.config(text="Download complete! You can input another link.")

def browse_path():
    folder_selected = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, folder_selected)

# GUI setup
root = tk.Tk()
root.title("YouTube Downloader - by kind4r")

# Watermark label in the bottom right corner
watermark_label = tk.Label(root, text="by kind4r", font=("Arial", 10), fg="gray", bg=root.cget("bg"))
watermark_label.pack(side="top", anchor="se", pady=0, padx=0)

# URL entry
url_label = tk.Label(root, text="Enter the URL of the video to download:")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Path entry
#default_path = r"E:\Downloads\Youtube_dl"
default_path = os.path.join(os.path.expanduser("~"), "Downloads")
path_label = tk.Label(root, text=f"Enter the path to save the file (default: {default_path}):")
path_label.pack()
path_entry = tk.Entry(root, width=50)
path_entry.pack()
browse_button = tk.Button(root, text="Browse", command=browse_path)
browse_button.pack()

# Format choice
format_label = tk.Label(root, text="Do you want to download the video or audio?")
format_label.pack()
format_var = tk.StringVar()
format_var.set("Audio")
video_radio = tk.Radiobutton(root, text="Video", variable=format_var, value="Video")
audio_radio = tk.Radiobutton(root, text="Audio", variable=format_var, value="Audio")
video_radio.pack()
audio_radio.pack()

# Download button
download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack()

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate", value=0)
progress_bar.pack()

# Result label
result_label = tk.Label(root, text="")
result_label.pack()

# Run the GUI
root.mainloop()

#pip install pyinstaller

#pyinstaller --onefile --icon=ytb.ico GUI.py
