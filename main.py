import subprocess as sb
import json
from pyfiglet import figlet_format
import questionary as q
from pathlib import Path
from rich.console import Console
from rich.text import Text

def get_input_path():
    c = q.text("Enter full path of the folder").ask()
    file_path = Path(c)

    if file_path.exists():
        print(f"The path '{file_path}' exists.")
    else:
        print(f"The path '{file_path}' does not exist.")
        exit()

    return file_path

def extd(path):
    for item in path.iterdir():
        a = item.resolve()
        if not a.is_file():
            continue
        command = ["exiftool", "-j", "-AllDates", "-FileCreateDate", str(a)]
        result = sb.run(command,shell = False,capture_output=True,text=True)
        print(result.stdout)
        data = json.loads(result.stdout)
        date_str = (
            data[0].get("DateTimeOriginal") or 
            data[0].get("CreateDate") or 
            data[0].get("ModifyDate") or
            data[0].get("FileCreateDate"))
        if date_str is None:
            print(f"No date found for {a.name}, skipping")
            continue
        if date_str == 'FileCreateDate':
            text = date_str.split('+')[0]
            text = date_str.replace(" ","_").replace(":","")
        else:
            text = date_str.replace(" ","_").replace(":","")
        a.rename(a.with_name(text+a.suffix))
    

path = get_input_path()
time = extd(path)

