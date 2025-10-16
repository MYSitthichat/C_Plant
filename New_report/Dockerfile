FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 libegl1 libglib2.0-0 \
    libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 \
    libxcb-keysyms1 libxcb-render-util0 libxcb-xinerama0 \
    libxcb-shape0 libxcb-xfixes0 libxcb-cursor0 \
    libfontconfig1 libdbus-1-3 \
    libatk-bridge2.0-0 libgtk-3-0 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "App.py"]