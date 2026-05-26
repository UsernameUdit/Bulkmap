import subprocess as sb
import json
import os
import json
from pyfiglet import figlet_format
from pathlib import Path
from rich.console import Console
from rich.text import Text
# from concurrent.futures import ThreadPoolExecutor
# import time will deal with concurrency once I complete this 

console = Console()
art = figlet_format("Bulkmap", font="slant")
text = Text(art)
text.stylize("bold rgb(220,0,0) on rgb(0,0,0)")
console.print(text)
console.print("Welcome to [italic red]Bulkmap[/italic red] \n")

def get_input_path():
    dangerous_dir = [Path("C:/"),
    Path("C:/Users"),
    Path("C:/Windows"),
    Path("C:/Program Files"),
    Path(os.path.expanduser("~"))]
    c = input("Enter full path of the folder")
    file_path = Path(c)

    if file_path.exists():
        print(f"The path '{file_path}' exists.")
    else:
        print(f"The path '{file_path}' does not exist.")
        exit()
    if file_path in dangerous_dir:
        print("Warning:System Directory Exiting.......")
        exit()
    return file_path


def extd(path):
    IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".raw"}
    VIDEO_FORMATS = {".mp4", ".mov", ".avi", ".mkv"}
    DOCUMENT_FORMATS = {".pdf", ".docx", ".txt"}
    for item in path.rglob('*'):
        a = item.resolve()
        if not a.is_file():
            continue
        file_count = sum(1 for a in path.rglob("*") if a.is_file())
        print(f"Bulkmap found {file_count} files")
        if (file_count > 5000):
            answer = input("Warning there are more than 5000 files in this directory Do you want to continue? (y/n): ").lower().strip()
            if answer in ['y', 'yes']:
                print("Continuing...")
            else:
                print("Exiting...")
                exit()
        command = ["exiftool", "-j", "-AllDates", "-FileCreateDate", str(a)]
        result = sb.run(command,shell = False,capture_output=True,text=True)
        print(result.stdout)
        data = json.loads(result.stdout)
        suffix = a.suffix.lower()

        if suffix in IMAGE_FORMATS:
            date_str = (
                        data[0].get("DateTimeOriginal") or
                        data[0].get("CreateDate") or
                        data[0].get("FileCreateDate"))

        elif suffix in VIDEO_FORMATS:
            date_str = (
                        data[0].get("FileCreateDate"))
        elif suffix in DOCUMENT_FORMATS:
            date_str = data[0].get("FileCreateDate")
        else:
            print(f"Unsupported format {a.name}, skipping")
            continue
        text = date_str.split('+')[0].replace(" ","_").replace(":","")
        new_path = a.with_name(text + a.suffix)
        counter = 1
        while new_path.exists():
            new_path = a.with_name(f"{text}_{counter}{a.suffix}")
            counter += 1
        a.rename(new_path)
        
path = get_input_path()
time = extd(path)

