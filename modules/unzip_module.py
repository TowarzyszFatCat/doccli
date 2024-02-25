from zipfile import ZipFile

def unzip():
    with ZipFile('_internal/mpv/mpv.zip','r') as file:
        file.extractall('_internal/mpv')