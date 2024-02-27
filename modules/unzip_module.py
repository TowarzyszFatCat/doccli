from zipfile import ZipFile


def unzip() -> None:
    with ZipFile('_internal/mpv/mpv.zip', 'r') as file:
        file.extractall('_internal/mpv')
