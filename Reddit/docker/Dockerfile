FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt .
RUN pip install -U setuptools
RUN pip install -r requirements.txt
COPY . /code

# Run main program.
#ENTRYPOINT ["python3", "./src/collect.py"]