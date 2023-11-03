import asyncio
import os.path
import time

from pyrogram.types import Message
import yt_dlp


async def download_video(url:str,user_id:str|int,msg_to_edit:Message):
    progress:float=0.0
    last_edit_time = 0

    def my_hook(d):
        nonlocal last_edit_time
        if d['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(d['filename']))
            print("Done downloading {}".format(file_tuple[1]))
        if d['status'] == 'downloading':
            p = d['_percent_str']
            p = p.replace('%', '')
            progress=str(p)

            current_time = time.time()
            if current_time - last_edit_time >= 1.0:
                last_edit_time = current_time
                print(d['filename'], d['_percent_str'], d['_eta_str'])

    temp_path = os.path.abspath('utils/temp')
    print(temp_path)
    if not os.path.isdir(temp_path+f'/{user_id}'):
        os.mkdir(f'{temp_path}/{user_id}')

    with yt_dlp.YoutubeDL() as ydl:
        info_dict=ydl.extract_info(url, download=False)
        video_url = info_dict.get("url", None)
        video_id = info_dict.get("id", None)
        video_title = info_dict.get('title', None)

    out_path=f'{temp_path}/{user_id}/{video_title}'
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '256'
        }],
        'postprocessor_args': [ '-vn', '-ar', '44100', '-ac', '2','-b:a','256k','-metadata',f'title={video_title}'],
        'outtmpl': f'{out_path}',
        'quiet': 'False',
        'noprogress': 'False',
        'progress_hooks':[my_hook]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


    return out_path + ".mp3", video_title