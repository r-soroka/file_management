import logging
import os
from pathlib import Path
import shutil
import argparse

parser = argparse.ArgumentParser(description='Organize a folder')
parser.add_argument(
    "directory",
    nargs="?",
    default=Path.cwd(),
    help="Directory to organize (defaults to current directory)"
)

args = parser.parse_args()

target = Path(args.directory)

if not target.exists() or not target.is_dir():
    parser.error(f"'{target}' is not a valid directory")

os.chdir(target)

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
    "Code": {".py", ".js", ".html", ".css", ".json", ".java", ".c", ".cpp", ".cs", ".r", ".ipynb", ".rmd"},
}

for category in CATEGORIES:
    if Path(category).exists():
        logging.debug(f"Directory {Path(category)}/ already exists; no action")
    else:
        Path(category).mkdir(exist_ok=True)
        logging.debug(f"Directory {Path(category)}/ does not exist; creating directory")

for item in list(Path.cwd().iterdir()):
    file_extension = item.suffix

    if not item.is_dir():
        for category, extensions in CATEGORIES.items():
            if file_extension.lower() in extensions:
                try:
                    shutil.move(item, category)
                    logging.info(f"Moved {item.name} -> {category}/")

                except shutil.Error as e:
                    count = 1
                    potential = Path(category) / f"{item.stem} ({count}){item.suffix}"

                    while potential.exists():
                        count += 1
                        potential = Path(category) / f"{item.stem} ({count}){item.suffix}"

                    try:
                        shutil.move(item, potential)
                        logging.info(f"Name taken; moved {item.name} -> {potential}")

                    except PermissionError as e:
                        logging.warning(
                            f"Failed to move {item.name} -> {category}/; access denied; {e}"
                        )

                except PermissionError as e:
                    logging.warning(
                        f"Failed to move {item.name} -> {category}/; access denied; {e}"
                    )

                break