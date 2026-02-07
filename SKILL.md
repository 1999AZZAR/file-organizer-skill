---
name: file-organizer
description: Organize files in directories by grouping them into folders based on their extensions or categories. Use when the user wants to clean up folders like Downloads, Desktop, or sort messy directories.
---

# File Organizer

This skill helps you organize messy directories by grouping files into logical subfolders based on their types.

## Workflows

### 1. Simple Organization
To organize a directory using default categories:
1. Identify the target directory.
2. Run the organization script: `python3 scripts/organize.py <directory>`

### 2. Custom Organization
To specify custom mappings for extensions:
1. Define a JSON mapping of folder names to lists of extensions.
2. Run the script with the `--mapping` flag:
   `python3 scripts/organize.py <directory> --mapping '{"Photos": [".jpg", ".png"], "Text": [".txt"]}'`

## Resources

- **`scripts/organize.py`**: A Python script that performs the actual file movement.
- **`references/categories.md`**: A list of common file extensions and their suggested categories.

## Best Practices

- Always verify the target directory exists before running the script.
- If the user specifies a directory that contains important system files, warn them before proceeding.
- Use `references/categories.md` to help the user decide how to group their files if they are unsure.