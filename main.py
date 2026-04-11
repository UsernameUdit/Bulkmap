import subprocess as sb
import json
from pyfiglet import figlet_format
import questionary as q
from pathlib import Path
from rich.console import Console
from rich.text import Text

def get_input_path():
    c = q.text("Enter full path of the image").ask()
    file_path = Path(c)

    if file_path.exists():
        print(f"The path '{file_path}' exists.")
    else:
        print(f"The path '{file_path}' does not exist.")
        exit()

    return file_path

def extd(path):
    command = ["exiftool","-j", "-AllDates",path]
    result = sb.run(command,shell = False,capture_output=True,text=True)
    print(result.stdout)
    data = json.loads(result.stdout)
    date_str = (data[0]["DateTimeOriginal"])
    text = date_str.replace(" ","_").replace(":","")
    return text

def rename(file_path,text):
    pass




path = get_input_path()
time= extd(path)
rename(path,time)
