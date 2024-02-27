from yt_dlp import YoutubeDL


def get_all_formats(url: str) -> list:
    with YoutubeDL({'quiet': True}) as ydl:
        info_dict: dict = ydl.extract_info(url, download=False)
        formats: list = info_dict['formats']

        available_formats: list = []

        # For CDA
        if 'cda' in url:
            for f in formats:
                format_info: list = [f['height'], f['url']]

                available_formats.append(format_info)


        # For sibnet
        elif 'sibnet' in url:
            for f in formats:
                format_info: list = ['Źródło (długie ładowanie)', f['http_headers']['Referer']]

                available_formats.append(format_info)


        # For google
        elif 'google' in url:
            for f in formats:
                format_info: list = []

                if f['format_id'] == 'source':
                    format_info.append('Źródło')
                    format_info.append(f['url'])
                    available_formats.append(format_info)


        # For mp4upload
        elif 'mp4upload' in url:
            for f in formats:
                format_info: list = ['Źródło (długie ładowanie)', f['http_headers']['Referer']]

                available_formats.append(format_info)

        # For dailymotion
        elif 'dailymotion' in url:
            for f in formats:
                format_info: list = [f['height'], f['url']]

                available_formats.append(format_info)

        else:
            print('Host nie jest wspierany!')
            exit()

        return available_formats
