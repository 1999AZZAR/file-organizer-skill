#!/usr/bin/env python3
import os
import shutil
import sys
import argparse
import json
import time
import logging
import hashlib
from datetime import datetime

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

class FileOrganizer:
    def __init__(self, directory, mapping=None, dry_run=False, by_date=False, recursive=False, deduplicate=False):
        self.root_dir = os.path.abspath(directory)
        self.dry_run = dry_run
        self.by_date = by_date
        self.recursive = recursive
        self.deduplicate = deduplicate
        self.mapping = mapping or self.get_default_mapping()
        self.history = []
        self.ignore_list = self.load_ignore_config()
        self.hashes = {} # For deduplication

    def get_default_mapping(self):
        return {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".odt"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
            "Video": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
            "Archives": [".zip", ".tar", ".gz", ".7z", ".rar", ".iso"],
            "Code": [".py", ".js", ".ts", ".html", ".css", ".json", ".yml", ".md", ".sh", ".sql", ".php"],
            "Executables": [".exe", ".msi", ".dmg", ".app", ".deb", ".rpm"]
        }

    def load_ignore_config(self):
        ignore = {'.git', 'node_modules', 'venv', '.openclaw', '__pycache__', 'organize_history.json'}
        ignore_file = os.path.join(self.root_dir, ".organizeignore")
        if os.path.exists(ignore_file):
            with open(ignore_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        ignore.add(line)
        return ignore

    def should_ignore(self, path):
        parts = os.path.relpath(path, self.root_dir).split(os.sep)
        return any(part in self.ignore_list for part in parts)

    def get_file_hash(self, file_path):
        """Generate SHA-256 hash for deduplication."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.error(f"Hash failed for {file_path}: {e}")
            return None

    def get_destination_folder(self, file_path):
        filename = os.path.basename(file_path)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        # Date-based Sorting
        if self.by_date:
            mtime = os.path.getmtime(file_path)
            dt = datetime.fromtimestamp(mtime)
            return os.path.join(self.root_dir, str(dt.year), dt.strftime("%m-%B"))

        # Extension-based Sorting
        for folder, extensions in self.mapping.items():
            if ext in extensions:
                return os.path.join(self.root_dir, folder)
        
        return os.path.join(self.root_dir, "Others")

    def handle_conflict(self, target_path):
        if not os.path.exists(target_path):
            return target_path
        
        base, ext = os.path.splitext(target_path)
        counter = 1
        while os.path.exists(f"{base}_{counter}{ext}"):
            counter += 1
        return f"{base}_{counter}{ext}"

    def process_file(self, file_path):
        if os.path.basename(file_path).startswith('.') and not self.recursive: return # Skip hidden in flat mode
        if self.should_ignore(file_path): return
        if file_path == __file__: return 

        # Deduplication Check
        if self.deduplicate:
            fhash = self.get_file_hash(file_path)
            if fhash:
                if fhash in self.hashes:
                    logger.info(f"[DEDUPLICATE] Killing waste: '{os.path.basename(file_path)}' is a duplicate of '{os.path.basename(self.hashes[fhash])}'")
                    if not self.dry_run:
                        try:
                            os.remove(file_path)
                            self.history.append({"action": "delete", "src": file_path, "reason": "duplicate"})
                        except Exception as e:
                            logger.error(f"Failed to delete duplicate {file_path}: {e}")
                    return
                else:
                    self.hashes[fhash] = file_path

        dest_dir = self.get_destination_folder(file_path)
        dest_path = os.path.join(dest_dir, os.path.basename(file_path))

        # Avoid moving if already in place
        if os.path.dirname(file_path) == dest_dir:
            return

        # Conflict Resolution
        final_dest = self.handle_conflict(dest_path)

        if self.dry_run:
            logger.info(f"[DRY RUN] Move '{os.path.basename(file_path)}' -> '{os.path.relpath(final_dest, self.root_dir)}'")
        else:
            try:
                os.makedirs(dest_dir, exist_ok=True)
                shutil.move(file_path, final_dest)
                logger.info(f"Moved: {os.path.basename(file_path)} -> {os.path.relpath(final_dest, self.root_dir)}")
                self.history.append({"action": "move", "src": file_path, "dst": final_dest})
            except Exception as e:
                logger.error(f"Error moving {file_path}: {e}")

    def run(self):
        logger.info(f"Scanning '{self.root_dir}'...")
        if self.dry_run: logger.info("--- DRY RUN MODE (No changes) ---")
        if self.deduplicate: logger.info("--- DEDUPLICATION ENABLED (Killing Waste) ---")

        if self.recursive:
            for root, dirs, files in os.walk(self.root_dir):
                # Prune ignored directories from walk
                dirs[:] = [d for d in dirs if not self.should_ignore(os.path.join(root, d))]
                for file in files:
                    self.process_file(os.path.join(root, file))
        else:
            for file in os.listdir(self.root_dir):
                path = os.path.join(self.root_dir, file)
                if os.path.isfile(path):
                    self.process_file(path)
        
        if not self.dry_run and self.history:
            self.save_log()

    def save_log(self):
        log_file = os.path.join(self.root_dir, "organize_history.json")
        with open(log_file, 'w') as f:
            json.dump(self.history, f, indent=2)
        logger.info(f"History saved to {log_file}")

    def undo(self, log_file):
        if not os.path.exists(log_file):
            logger.error("Log file not found.")
            return

        with open(log_file, 'r') as f:
            history = json.load(f)
        
        logger.info(f"Undoing {len(history)} operations...")
        for item in reversed(history):
            if item['action'] == 'move':
                src = item['src']
                dst = item['dst']
                try:
                    if os.path.exists(dst):
                        os.makedirs(os.path.dirname(src), exist_ok=True)
                        shutil.move(dst, src)
                        logger.info(f"Restored: {os.path.basename(dst)} -> {os.path.dirname(src)}")
                except Exception as e:
                    logger.error(f"Failed to restore {dst}: {e}")
            elif item['action'] == 'delete':
                logger.warning(f"Note: Cannot undo deletion of duplicate '{os.path.basename(item['src'])}'.")
        
        os.remove(log_file)
        logger.info("Undo complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Professional File Organizer")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to organize")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without moving")
    parser.add_argument("--date", action="store_true", help="Organize by Year/Month")
    parser.add_argument("--recursive", action="store_true", help="Deep scan")
    parser.add_argument("--deduplicate", action="store_true", help="Kill duplicate files (SHA-256)")
    parser.add_argument("--undo", help="Undo changes using history file")
    
    args = parser.parse_args()
    
    organizer = FileOrganizer(args.directory, dry_run=args.dry_run, by_date=args.date, recursive=args.recursive, deduplicate=args.deduplicate)
    
    if args.undo:
        organizer.undo(args.undo)
    else:
        organizer.run()
