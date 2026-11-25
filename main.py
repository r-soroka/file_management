import logging
import os
from pathlib import Path
import shutil

logging.basicConfig(level=logging.INFO)

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic", ".bmp"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".md", ".rtf", ".odt"},
    "Spreadsheets": {".xlsx", ".xls", ".csv", ".ods"},
    "Slides": {".pptx", ".ppt", ".odp"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Installers": {".exe", ".msi", ".dmg", ".deb"},
    "Audio": {".mp3", ".wav", ".flac", ".m4a", ".ogg"},
    "Video": {".mp4", ".mkv", ".mov", ".avi", ".webm"},
    "Code": {".py", ".js", ".html", ".css", ".json", ".java", ".c", ".cpp", ".cs", ".r", ".ipynb"},
}

# cwd = Path.home() / "Downloads"

new_cwd = Path.cwd() / "test"
os.chdir(new_cwd)
for category in CATEGORIES:
    if Path(category).exists():
        logging.debug(f"Directory {Path(category)}/ already exists; no action")
    else:
        Path(category).mkdir(exist_ok=True)
        logging.debug(f"Directory {Path(category)}/ does not exist; creating directory")

for item in list(new_cwd.iterdir()):
    file_extension = os.path.splitext(item)[1]
    if not item.is_dir():
        for category, extensions in CATEGORIES.items():
            if file_extension.lower() in extensions:
                try:
                    shutil.move(item, category)
                    logging.info(f"Moved {item.name} -> {category}/")
                except  shutil.Error:
                    count = 1
                    potential = Path(category) / f"{item.stem} ({count}){item.suffix}"
                    while potential.exists():
                        count += 1
                        potential = Path(category) / f"{item.stem} ({count}){item.suffix}"

                    shutil.move(item, potential)
                    logging.info(f"Name taken; moved {item.name} -> {potential}")
                except PermissionError as e:
                    logging.warning(f"Failed to move {item.name} -> {category}/; access denied; {e}")

                break