FROM ubuntu:25.10

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir -r /app/requirements.txt

EXPOSE 5555

#CMD ["python", "main.py"]
