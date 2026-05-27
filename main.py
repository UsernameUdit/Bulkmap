import subprocess as sb
import json
import os
import json
from pyfiglet import figlet_format
from datetime import datetime
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
    c = console.input("[bold red]Enter full path of the folder:[/] ")
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
    log = []
    file_count = sum(1 for a in path.rglob("*") if a.is_file())
    print(f"Bulkmap found {file_count} files")
    if (file_count > 5000):
            answer = input("Warning there are more than 5000 files in this directory Do you want to continue? (y/n): ").lower().strip()
            if answer in ['y', 'yes']:
                print("Continuing...")
            else:
                print("Exiting...")
                exit()
    for item in path.rglob('*'):
        a = item.resolve()
        if not a.is_file():
            continue
        command = ["exiftool", "-j", "-AllDates", "-FileCreateDate", "-filename", str(a)]
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
        log.append({"original": str(a), "new_name": text + a.suffix})
    return log


def log_writer(log_entries,out_dir):
    folder_name = out_dir.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = out_dir / f"bulkmap_{folder_name}_{timestamp}.json"
    with open(log_path,"w") as f:
        json.dump(log_entries,f,indent=4)


path = get_input_path()
log = extd(path)
log_writer(log,path)

