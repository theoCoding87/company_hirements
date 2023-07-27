FROM python:3

WORKDIR /app

RUN pip install fpdf tabulate

CMD ["python", "skript.py"]

COPY . /app
