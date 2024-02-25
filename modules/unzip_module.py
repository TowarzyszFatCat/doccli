from zipfile import ZipFile

def unzip():
    with ZipFile('mpv/mpv.zip','r') as file:
        file.extractall('mpv')