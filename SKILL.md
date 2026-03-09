---
name: file-organizer-skill
description: Organize files in directories by grouping them into folders based on their extensions or date. Includes Dry-Run, Recursive, Deduplication, and Smart Ignore capabilities.
---

# File Organizer (Evil Edition)

## Features
- **Smart Sorting**: Group by Extension (Default) or Date (Year/Month).
- **Deduplication (Evil)**: Kill waste by deleting identical files based on SHA-256 hash.
- **Smart Ignore**: Automatically skips `.git`, `node_modules`, `venv`, and supports custom `.organizeignore` files.
- **Safety**: Conflict resolution (auto-rename), Dry Run mode, and Undo capability.
- **Deep Clean**: Recursive scanning with directory pruning.
- **Audit**: Generates `organize_history.json` for tracking.

## Usage

### Basic Sort (by Extension)
```bash
python3 scripts/organize.py /path/to/folder
```

### Date Sort (Year/Month)
Great for photos or archives.
```bash
python3 scripts/organize.py /path/to/folder --date
```

### Recursive Clean with Deduplication (Evil Mode)
Clean everything and delete duplicates.
```bash
python3 scripts/organize.py /path/to/folder --recursive --deduplicate
```

### Dry Run (Simulate)
See what *would* happen without moving or deleting anything.
```bash
python3 scripts/organize.py /path/to/folder --dry-run
```

### Undo
Revert changes using the history file (Note: deleted duplicates cannot be restored).
```bash
python3 scripts/organize.py --undo /path/to/folder/organize_history.json
```

## Config
Modify `scripts/organize.py` `get_default_mapping()` to add custom extensions.
