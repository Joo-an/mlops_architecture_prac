FROM python:3.9
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    gcc \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*
# pip 업그레이드
RUN pip install --upgrade pip
# numpy만 먼저 설치 (빌드 헤더 필요함)
RUN pip install numpy==1.21.0
# numpy 설치 후 numpy 헤더 인식 경로 설정
ENV CFLAGS="-I/usr/local/lib/python3.9/site-packages/numpy/core/include"
# requirements.txt 나머지 설치
COPY requirements.txt .
RUN pip install -r requirements.txt
# 앱 코드 복사
WORKDIR /js-fastapi-monitoring
COPY . .
EXPOSE 80
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "80"]