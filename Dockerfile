FROM python:3

WORKDIR /

COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "app/create_db.py"]
CMD [ "python", "-m", "app.main"]
