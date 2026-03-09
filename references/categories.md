# File Categories (Evil Edition Reference)

This reference maps file signatures and extensions to their optimized containment zones.

## Core Categories

| Zone | Extensions | Description |
| --- | --- | --- |
| **Images** | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .heic, .tiff, .raw | Visual assets and captures. |
| **Documents** | .pdf, .doc, .docx, .txt, .rtf, .xls, .xlsx, .ppt, .pptx, .csv, .odt, .epub | Standard data and text containers. |
| **Audio** | .mp3, .wav, .flac, .aac, .ogg, .m4a, .wma | Sonic data. |
| **Video** | .mp4, .mkv, .mov, .avi, .webm, .wmv, .flv, .m4v | Motion sequences. |
| **Archives** | .zip, .tar, .gz, .7z, .rar, .iso, .bz2, .xz | Compressed containers. |
| **Code** | .py, .js, .ts, .html, .css, .json, .yml, .yaml, .md, .sh, .sql, .php, .rs, .go, .c, .cpp, .h, .java | Source material and configurations. |
| **Executables** | .exe, .msi, .dmg, .app, .deb, .rpm, .bin, .sh, .appimage | Compiled logic and installers. |
| **Fonts** | .ttf, .otf, .woff, .woff2, .eot | Typographic definitions. |
| **Models/3D** | .stl, .obj, .fbx, .blend, .step, .skp | Spatial and 3D print definitions. |
| **Design** | .psd, .ai, .fig, .xd, .sketch | Original design source files. |

## Evil Protocols

### Deduplication
The system uses **SHA-256 fingerprinting** to identify redundant data. 
- Identical content across different filenames triggers **waste termination**.
- Only the primary instance (usually the first one encountered or the one with the shortest name) is preserved.

### Smart Ignore
The following constructs are treated as **Immutable Infrastructure** and bypassed:
- **`Version Control`**: `.git`, `.svn`, `.hg`
- **`Dependencies`**: `node_modules`, `venv`, `.venv`, `__pycache__`
- **`System`**: `.DS_Store`, `Thumbs.db`, `.openclaw`
- **`Custom`**: Any entry defined in `.organizeignore`

---
_Redundancy is the enemy of progress._
