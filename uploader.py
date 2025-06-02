from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend

videos = [
    # {
    #     'video': 'Download/2025-02-19 22.23.35-视频-夜阑听声FM-如果日语歌曲有天花板，那么哪一首...奏一响拾起多少人的回忆 #音乐分享.mp4',
    #     'description': '夜阑听声FM'
    # },
    {
        'video': 'Download/2018年的夏天究竟有怎样的魔力总能...拾起多少人的回忆.mp4',
        'description': '夜阑听声FM #童话镇 #起风了'
    }
]

if __name__ == '__main__':
    auth = AuthBackend(cookies='cookies.txt')
    failed_videos = upload_videos(videos=videos, auth=auth)

    for video in failed_videos:  # each input video object which failed
        print(f"{video['video']} with description {video['description']} failed")