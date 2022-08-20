FROM python:3

WORKDIR /src

COPY app/requirements.txt .
RUN pip install -r app/requirements.txt

COPY . .

CMD [ "python", "app/main.py"]
