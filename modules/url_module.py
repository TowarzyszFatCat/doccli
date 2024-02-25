from yt_dlp import YoutubeDL
from time import sleep

def get_all_formats(url):
    with YoutubeDL({'quiet': True}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict['formats']

        aviable_formats = []


        # For CDA
        if 'cda' in url:
            for format in formats:
                format_info = []

                format_info.append(format['height'])
                format_info.append(format['url'])
                aviable_formats.append(format_info)


        # For sibnet
        elif 'sibnet' in url:
            for format in formats:
                format_info = []

                format_info.append('Źródło (długie ładowanie)')
                format_info.append(format['http_headers']['Referer'])   # Sibnet link is in Referer!
                aviable_formats.append(format_info)


        # For google
        elif 'google' in url:
            for format in formats:
                format_info = []
                if format['format_id'] == 'source':
                    format_info.append('Źródło')
                    format_info.append(format['url'])
                    aviable_formats.append(format_info)

        # For mp4upload
        elif 'mp4upload' in url:
            for format in formats:
                format_info = []

                format_info.append('Źródło (długie ładowanie)')
                format_info.append(format['http_headers']['Referer'])
                aviable_formats.append(format_info)

        # For dailymotion
        elif 'dailymotion' in url:
            for format in formats:
                format_info = []

                format_info.append(format['height'])
                format_info.append(format['url'])
                aviable_formats.append(format_info)

        else:
            print('Host nie jest wspierany!')
            exit()

        return aviable_formats
