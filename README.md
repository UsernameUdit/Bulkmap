# Bulkmap

A solution for a problem that don't exist renaming your file names to their date of creation. Bulkmap does that really well just give your absolute file path to it.

<img width="1013" height="155" alt="welcometobulkmap" src="https://github.com/user-attachments/assets/23db2ef9-ef8b-42bb-b7ea-377ea6359fc8" />

# Working

Bulkmap validates your filepath, count the number of files in a folder and subfolders give the filepath to exiftool to extract their creation date in json file format and writes a json log about each file what was its original name and new name. if you don't want to change filenames you can use the '--dry-run' flag to generate a json log file.

# Sauce
Install exiftool from www.exiftool.org

1. Requirements
   '''pip install -r requirements.txt'''
2. Running the script
   ''' python3 main.py'''
3. for dryrun
   '''python3 main.py --dry-run'''
