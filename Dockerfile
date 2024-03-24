FROM python:3.12

ADD main.py .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./main.py"]
