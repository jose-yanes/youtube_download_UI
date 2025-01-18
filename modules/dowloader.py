import json
import yt_dlp
from yt_dlp.postprocessor import FFmpegPostProcessor
FFmpegPostProcessor._ffmpeg_location.set(r'../ffmpegytdlp/')



def download_pending(pending_list):

    pending_videos = []
    pending_audio = []

    print(f"Pending List: {pending_list}")

    for url in pending_list:
        print(f"URL: {url}")
        if url["format"] == "video":
            pending_videos.append(url["url"])
        elif url["format"] == "audio":
            pending_audio.append(url["url"])

    print(f"Videos: {pending_videos}")
    print(f"Audio: {pending_audio}")



    if pending_videos:

        ydl_opts = {
            'paths': {"home": "videos"},
            'writethumbnail': True,
            'writeinfojson': True,
            'writethumbnail': True,
            'embed-thumbnail': True,
            'postprocessors': [
                {'key': 'FFmpegMetadata', 'add_metadata': True,
                },
                {'key': 'EmbedThumbnail', 'already_have_thumbnail': False,}
            ]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(pending_videos)

        if error_code:
            print("Some Video Failed to download")
            return 400
        else:
            # Agregar tema de cambiar el status en la base etc y feedback al usuario
            print("All videos successfully downloaded")
            return 200

    if pending_audio:

        ydl_opts = {
            "paths": {"home": "music"},
            'extract_audio': True,
            'format': 'mp3/bestaudio/best',
            'writethumbnail': True,
            'embed-thumbnail': True,
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'},
                {'key': 'EmbedThumbnail', 'already_have_thumbnail': False},
                {'key': 'FFmpegMetadata', 'add_metadata': True}
            ]
            }


        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(pending_audio)

            if error_code:
                print("Some Audio Failed to download")
                return 400
            else:
                print("All Audio successfully downloaded")
                return 200

def get_info(link):
    with yt_dlp.YoutubeDL() as video:
        info_video = video.extract_info( link, download = False )
        return info_video