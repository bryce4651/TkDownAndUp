from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend

videos = [
    # {
    #     'video': 'Download/2025-02-19 22.23.35-视频-夜阑听声FM-如果日语歌曲有天花板，那么哪一首...奏一响拾起多少人的回忆 #音乐分享.mp4',
    #     'description': '夜阑听声FM'
    # },
    {
        'video': 'Download/vide/显眼宝-唐僧啃自己指甲能长生不老吗.mp4',
        'description': '#显眼宝 #反转搞笑 #西游内传'
    }
]

if __name__ == '__main__':
    proxy = {'host': '172.31.190.200', 'port': '63080'}
    auth = AuthBackend(cookies='cookies.txt')
    failed_videos = upload_videos(videos=videos, auth=auth, proxy=proxy, headless=True)

    for video in failed_videos:  # each input video object which failed
        print(f"{video['video']} with description {video['description']} failed")
