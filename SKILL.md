# File Organizer (Professional Edition)

## Features
- **Smart Sorting**: Group by Extension (Default) or Date (Year/Month).
- **Deduplication**: Identify and remove identical files based on SHA-256 fingerprinting to optimize storage.
- **Smart Ignore**: Automatically skips development and system directories (`.git`, `node_modules`, `venv`, etc.) and supports custom `.organizeignore` files.
- **Safety**: Includes Conflict Resolution (auto-rename), Dry Run simulation, and Undo capabilities.
- **Recursive Clean**: Deep scanning with intelligent directory pruning.
- **Audit Logging**: Generates `organize_history.json` for precise operation tracking.

## Usage

### Basic Sort (by Extension)
```bash
python3 scripts/organize.py /path/to/folder
```

### Date Sort (Year/Month)
```bash
python3 scripts/organize.py /path/to/folder --date
```

### Recursive Clean with Deduplication
```bash
python3 scripts/organize.py /path/to/folder --recursive --deduplicate
```

### Dry Run (Simulate)
```bash
python3 scripts/organize.py /path/to/folder --dry-run
```

### Undo
Revert changes using the history file (Note: deleted duplicates cannot be restored).
```bash
python3 scripts/organize.py --undo /path/to/folder/organize_history.json
```
