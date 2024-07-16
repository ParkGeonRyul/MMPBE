# Python 3.12.4 이미지 사용
FROM python:3.12.4

# env 설정
ENV MONGO_DATABASE=$[variable-FastAPI.MONGO_DATABASE]
ENV MONGO_HOST=$[variable-FastAPI.MONGO_HOST]
ENV MONGO_PASSWORD=$[variable-FastAPI.MONGO_PASSWORD]
ENV MONGO_USERNAME=$[variable-FastAPI.MONGO_USERNAME]
ENV MS_CLIENT_ID=$[variable-FastAPI.MS_CLIENT_ID]
ENV MS_CLIENT_SECRET=$[variable-FastAPI.MS_CLIENT_SECRET]
ENV MS_CLIENT_SECRET_=$[variable-FastAPI.MS_CLIENT_SECRET_]
ENV MS_CLIENT_VALUE_=$[variable-FastAPI.MS_CLIENT_VALUE_]
ENV MS_REDIRECT_URI=$[variable-FastAPI.MS_REDIRECT_URI]

# 디렉토리 설정
WORKDIR /code

# requirements.txt 파일을 /app 디렉토리로 복사
COPY ./requirements.txt /code/requirements.txt

# 필요 라이브러리 설치
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY app .

# uvicorn 서버 실행
CMD ["sh", "dev.bash"]