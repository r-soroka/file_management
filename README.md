# File Organizer

A small command-line tool that sorts the files in a folder into category subfolders (Images, Documents, Code, and so on) based on each file's extension. I built it to clean up my Downloads folder. It's v1 of a larger personal file management system.

## What it does

Point it at a folder and it:

1. Creates a subfolder for each category (`Images`, `Documents`, `Spreadsheets`, `Slides`, `Archives`, `Installers`, `Audio`, `Video`, `Code`).
2. Looks at each file **directly inside** the folder and matches its extension (case-insensitive) to a category.
3. Moves the file into that category's folder.
4. If a file with the same name is already there, it **never overwrites**. It renames the incoming file to the next free name: `screenshot.png` → `screenshot (1).png` → `screenshot (2).png`.
5. Logs every move, every rename, and every file it couldn't move, with the reason.

## Usage

Requires Python 3.8 or newer. There are no third-party packages to install.

```
python organize.py [directory]
```

| Argument | Description |
| --- | --- |
| `directory` | Folder to organize. Optional; defaults to the current directory. |
| `-h`, `--help` | Show usage and exit. |

Examples:

```
python organize.py C:\Users\you\Downloads
python organize.py "C:\Users\you\Desktop\messy folder"
```

### Running it as a command on Windows

`organize.bat` is a small wrapper that runs `organize.py` from the same folder and passes along any arguments. Add this project's folder to your `PATH` and you can run it from any terminal:

```
organize C:\Users\you\Downloads
```

## Categories

| Folder | Extensions |
| --- | --- |
| Images | .jpg .jpeg .png .gif .webp .svg .heic .bmp |
| Documents | .pdf .docx .doc .txt .md .rtf .odt |
| Spreadsheets | .xlsx .xls .csv .ods |
| Slides | .pptx .ppt .odp |
| Archives | .zip .rar .7z .tar .gz |
| Installers | .exe .msi .dmg .deb |
| Audio | .mp3 .wav .flac .m4a .ogg |
| Video | .mp4 .mkv .mov .avi .webm |
| Code | .py .js .html .css .json .java .c .cpp .cs .r .ipynb .rmd |

To change the categories, edit the `CATEGORIES` dictionary at the top of `organize.py`. Each extension should appear in only one category.

## Design decisions

- **Top level only.** It never goes into subfolders. Folders you've already organized, like an unzipped project, stay intact, and the category folders it creates are never re-sorted.
- **Unknown files stay put.** Files whose extension isn't in any category aren't moved. There is no catch-all "Other" folder, so the tool only acts on files it can classify with confidence.
- **Hidden files and partial downloads are left alone.** Files like `.DS_Store`, and in-progress downloads (`.crdownload`, `.part`), don't match any category, so they're never moved. Moving a file that's still downloading would break the download.
- **No overwriting, ever.** Name collisions are resolved by numbering, using the lowest free number for each file, matching how Windows names copies.
- **The file list is taken before anything moves,** so moving files can't cause the loop to skip or repeat items.
- **Locked files don't stop the run.** On Windows, a file open in another program can't be moved. The tool logs a warning with the system's error message and carries on. Close the program and run it again to pick that file up.

## Example log

```
INFO:root:Moved notes.txt -> Documents/
INFO:root:Moved IMG_2041.JPG -> Images/
INFO:root:Name taken; moved screenshot.png -> Images\screenshot (1).png
WARNING:root:Failed to move report.pdf -> Documents/; access denied; [WinError 32] The process cannot access the file because it is being used by another process: ...
```

## Known limitations

- **Every category folder is created on each run,** even if no files go into it.
- **Compound extensions use only the last part.** `backup.tar.gz` is matched by `.gz`, and a collision would be named `backup.tar (1).gz`.
- **There's no preview mode.** Files are moved as soon as it runs. Try it on a copy of a folder first.
- **Running it with no argument organizes the folder you're in,** so check your current directory first.

## Planned (v2)

- `--dry-run` flag to preview every move without changing anything
- Categories loaded from a config file instead of the script
- Only create category folders when a file actually goes into them
- Duplicate-file detection by content hash
- Unit tests with `pytest`
