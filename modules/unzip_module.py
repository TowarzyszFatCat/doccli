from zipfile import ZipFile
import logging
logging.basicConfig(
    filename="doccli.log", filemode="w", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
    )


def unzip() -> None:

    logging.info(msg="Proba rozpakowania mpv")

    with ZipFile('_internal/mpv/mpv.zip', 'r') as file:
        file.extractall('_internal/mpv')

        logging.info(msg="Wypakowano mpv")