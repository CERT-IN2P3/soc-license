FROM python:3

EXPOSE 8000

WORKDIR /usr/src/app

COPY . .

RUN pip install -r tools/requirements.txt --no-cache-dir

WORKDIR /usr/src/app/soc_license
RUN mkdir data
RUN mkdir data/diplomas

RUN python manage.py migrate
RUN python manage.py loaddata ../tools/initial-data.json
RUN pyrsa-keygen --out=./config/diploma.key --pubout=./config/diploma.pub 2048

ENTRYPOINT ["python3"]
CMD ["scripts/start.sh"]