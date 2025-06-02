FROM alpine:latest

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN \
   apk add -u --no-cache bind-tools python3 py3-pip && \
   pip install --no-cache-dir --break-system-packages -r requirements.txt
COPY main.py .

CMD ["fastapi", "run", "main.py", "--host", "", "--port", "8000"]
