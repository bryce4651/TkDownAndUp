import time
from asyncio import CancelledError
from asyncio import run

from src.application import TikTokDownloader
from src.application import APIServer
from src.models import Account

from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend


async def main():
    async with TikTokDownloader() as downloader:
        downloader.project_info()
        downloader.check_config()
        await downloader.check_settings(
            False,
        )
        try:
            acc = Account(
                sec_user_id="MS4wLjABAAAAIqOcUlkHRYn3R9QrxuXwCrQbarxTKLqYNDByv_hGbGU",
                count=10,
            )
            api_server = APIServer(downloader.parameter, downloader.database)
            resp = await api_server.handle_account(acc)
            if len(resp.data) == 0:
                print("未找到任何作品")
                return
            i = 0
            for data in resp.data:
                i += 1
                _id = data["id"]
                res = await api_server.detail_inquire([_id])
                print("====>", res)
                time.sleep(10)
                filename = f"{data['type']}-{data['nickname']}-{data['desc']}.mp4"
                print("====> filename:", filename)
                video = {
                    'video': f'Download/{filename}',
                    'description': data["desc"]
                }
                auth = AuthBackend(cookies='cookies.txt')
                failed_videos = upload_videos(
                    videos=[video], auth=auth,
                    # proxy=proxy,
                    headless=True)

                for video in failed_videos:  # each input video object which failed
                    print(f"{video['video']} with description {video['description']} failed")
                if i >= 3:
                    return
        except (
                KeyboardInterrupt,
                CancelledError,
        ):
            return


if __name__ == "__main__":
    run(main())
