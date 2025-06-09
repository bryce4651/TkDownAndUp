import asyncio
import os
import random
import time
from asyncio import CancelledError
from asyncio import run

from src.application import TikTokDownloader
from src.application import APIServer
from src.models import Account
from src.config import Settings
from src.tools import ColorfulConsole, ExistedError
from src.custom import PROJECT_ROOT

from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend

async def run_task(downloader: TikTokDownloader, sec_user_id: str, cookie_file: str = "cookies.txt"):
    try:
        acc = Account(
            sec_user_id=sec_user_id,
            # count=10,
        )
        api_server = APIServer(downloader.parameter, downloader.database)
        await asyncio.sleep(random.randint(1, 30)*3)
        resp = await api_server.handle_account(acc)
        if len(resp.data) == 0:
            print("未找到任何作品")
            return
        i = 0
        for data in resp.data:
            i += 1
            if i < 3:
                continue
            _id = data["id"]
            filename = f"{data['type']}-{data['nickname']}-{data['desc']}.mp4"
            try:
                await asyncio.sleep(random.randint(5, 300)*3)
                res = await api_server.detail_inquire([_id])
            except ExistedError:
                print("===>skip file: ", filename)
                continue
            await asyncio.sleep(10)
            print("====> filename:", filename)
            video = {
                'video': f'Download/{filename}',
                'description': data["desc"]
            }
            if not os.path.exists(f'Download/{filename}'):
                continue
            auth = AuthBackend(cookies_str=cookie_file)
            failed_videos = upload_videos(
                videos=[video], auth=auth,
                # proxy=proxy,
                headless=True)

            for video in failed_videos:  # each input video object which failed
                print(f"{video['video']} with description {video['description']} failed")
            if os.path.exists(filename):
                os.remove(filename)
                print("文件已删除:", filename)
            else:
                print("文件不存在:", filename)
            await asyncio.sleep(4 * 3600)
    except (
            KeyboardInterrupt,
            CancelledError,
    ):
        return


async def run_job(data: dict):
    async with TikTokDownloader() as downloader:
        downloader.project_info()
        downloader.check_config()
        await downloader.check_settings(
            False,
        )
        await run_task(downloader, data["sec_user_id"], data["cookie_file"])


async def main():
    tasks = [
        run_job(data)
        for data in Settings(PROJECT_ROOT, ColorfulConsole()).read()["tiktok_account_settings"]
    ]
    try:
        await asyncio.gather(*tasks)  # 并发运行
    except (KeyboardInterrupt, CancelledError):
        print("取消并退出程序")
    return


if __name__ == "__main__":
    run(main())
