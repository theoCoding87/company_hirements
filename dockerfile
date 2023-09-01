FROM python:3

WORKDIR /app

RUN pip install fpdf tabulate

#directory for data persistance, i.e. the path to the directory outside of the container
VOLUME [ "/app/export" ]

COPY . .

CMD ["python", "skript.py"]



# build command: docker build -t fashion-accounts .
# run command:  docker run --rm -it -v export:/app/export
                # absolute_path:mappe_path