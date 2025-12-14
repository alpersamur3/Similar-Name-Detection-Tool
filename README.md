# Similar Name Detection Tool

A lightweight Python desktop tool that scans folders, intelligently groups files and folders by name similarity (exact or fuzzy), and helps you clean up duplicates quickly.

## Features

- Recursive scanning of folders and subfolders
- Scan modes: Files only, Folders only, or Both
- Grouping options:
  - Exact name + same extension
  - Similar name + same extension (Levenshtein distance)
  - Similar name only
- Adjustable similarity threshold (default: 4)
- Minimum file size filter (default: 1 MB)
- Powerful extension filtering:
  - Predefined checkboxes for images, videos, documents, archives, audio, and more
  - Custom extensions (add/remove via text field)
  - Include only selected or exclude selected extensions
- Results shown in expandable tree view with group totals (item count + size)
- Quick actions:
  - Double-click: Open containing folder
  - Right-click menu: Open item, Open containing folder, Copy full path
- Real-time scanning progress
- Maximized window on startup
- Fully cross-platform (Windows, macOS, Linux)

## Screenshot

<img width="1911" height="1143" alt="image" src="https://github.com/user-attachments/assets/91e89c34-f2ba-48a9-9f5f-8eb673478c47" />


## Requirements

- Python 3.6 or higher
- `jellyfish` library

Install the dependency:
```
pip install jellyfish
```
## Usage

Save the script as similar_name_tool.py

Run it:
```
python similar_name_tool.py
```
Browse and select a folder

Adjust settings (extensions, threshold, size filter, etc.)

Click Start Scan

Explore results and use right-click/double-click for fast access

Ideal for organizing large drives, finding naming conflicts, and removing duplicate or near-duplicate files.
## Contributing
Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.
## Star the Repo
If you find this tool useful, please give it a ⭐ on GitHub! It helps others discover it.

Thank you for using Similar Name Detection Tool!
