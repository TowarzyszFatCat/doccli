from zipfile import ZipFile
import logging
import modules.global_variables_module as gvm
logging.basicConfig(
    filename=gvm.LOG_PATH, filemode="w", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
    )


def unzip() -> None:

    logging.info(msg="Proba rozpakowania mpv")

    with ZipFile('mpv/mpv.zip', 'r') as file:
        file.extractall('_internal/mpv')

        logging.info(msg="Wypakowano mpv")