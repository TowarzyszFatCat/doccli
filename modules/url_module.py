import time

from yt_dlp import YoutubeDL

import logging
import modules.global_variables_module as gvm
logging.basicConfig(
    filename=gvm.LOG_PATH, filemode="w", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
    )


def get_all_formats(url: str) -> list:

    logging.info(msg="Pobieranie dostepnych formatow...")

    with YoutubeDL({'quiet': True}) as ydl:
        info_dict: dict = ydl.extract_info(url, download=False)
        logging.debug(msg=f"info_dict: {info_dict}")

        #formats: list = info_dict['formats']

        available_formats: list = []

        # For CDA
        if 'cda' in url:

            logging.info(msg="Wykryto cda")
            formats: list = info_dict['formats']

            for f in formats:
                format_info: list = [f['height'], f['url']]
                print(format_info)

                available_formats.append(format_info)

        # For sibnet
        elif 'sibnet' in url:

            logging.info(msg="Wykryto sibnet")

            headers = info_dict['http_headers']
            ref = headers['Referer']

            format_info: list = ['Źródło (długie ładowanie)', ref]

            available_formats.append(format_info)


        # For google
        # elif 'google' in url:
        #
        #     logging.info(msg="Wykryto google drive")
        #
        #     for f in formats:
        #         format_info: list = []
        #
        #         if f['format_id'] == 'source':
        #             format_info.append('Źródło')
        #             format_info.append(f['url'])
        #             available_formats.append(format_info)
        #
        # # For mp4upload
        # elif 'mp4upload' in url:
        #
        #     logging.info(msg="Wykryto mp4upload")
        #
        #     for f in formats:
        #         format_info: list = ['Źródło (długie ładowanie)', f['http_headers']['Referer']]
        #
        #         available_formats.append(format_info)
        #
        # # For dailymotion
        # elif 'dailymotion' in url:
        #
        #     logging.info(msg="Wykryto dailymotion")
        #
        #     for f in formats:
        #         format_info: list = [f['height'], f['url']]
        #
        #         available_formats.append(format_info)

        else:
            print('Host nie jest wspierany!')
            logging.info(msg="Wykryto niewspieranego hosta!")
            exit()

        logging.info(msg=f"Dostepne formaty: {available_formats}")

        return available_formats
