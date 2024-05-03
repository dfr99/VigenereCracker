FROM python@sha256:d75047a8c6f2d928693fcf808758818fed314eb4410b062d8d1c82cafd79fe9a

WORKDIR /usr/src/app

COPY code/ .

RUN apk add poetry=1.7.1-r0 --no-cache && \
poetry install

ENTRYPOINT ["python", "vigenerecracker/EstrellasFugaces.py"]
