FROM python:3.12-slim

LABEL name="DouK-Downloader" authors="JoeanAmier" repository="https://github.com/JoeanAmier/TikTokDownloader"

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5555

#CMD ["python", "main.py"]
