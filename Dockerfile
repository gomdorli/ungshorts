FROM python:3.11-slim
WORKDIR /usr/src/app

# 환경 변수에 BASE_PATH가 있으면 패키지 캐싱 최소화
COPY shared shared/
COPY bot bot/
COPY keywords keywords/
COPY content content/
COPY video video/
COPY uploader uploader/
COPY stats stats/
COPY utils utils/
COPY webserver/requirements.txt webserver/requirements.txt
COPY worker/requirements.txt worker/requirements.txt
COPY webserver webserver/
COPY worker worker/
COPY Dockerfile README.md .

# Webservice와 Worker 공통 의존성 설치
RUN pip install --no-cache-dir -r webserver/requirements.txt \
    && pip install --no-cache-dir -r worker/requirements.txt

ENTRYPOINT ["python"]