import os
import shutil
import sys
import argparse
import json

def organize_files(directory, mapping):
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isdir(filepath):
            continue

        _, extension = os.path.splitext(filename)
        extension = extension.lower()

        target_folder = None
        for folder, extensions in mapping.items():
            if extension in extensions:
                target_folder = folder
                break
        
        if not target_folder:
            target_folder = "Others"

        target_path = os.path.join(directory, target_folder)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        try:
            shutil.move(filepath, os.path.join(target_path, filename))
            print(f"Moved: {filename} -> {target_folder}/")
        except Exception as e:
            print(f"Error moving {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files in a directory by extension.")
    parser.add_argument("directory", help="The directory to organize")
    parser.add_argument("--mapping", help="JSON string mapping folders to extensions")
    
    args = parser.parse_args()
    
    if args.mapping:
        mapping = json.loads(args.mapping)
    else:
        # Default mapping
        mapping = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
            "Video": [".mp4", ".mkv", ".mov", ".avi"],
            "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
            "Code": [".py", ".js", ".ts", ".html", ".css", ".json", ".yml", ".md"],
        }
    
    organize_files(args.directory, mapping)
