FROM python:3.11.5

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080
ENTRYPOINT ["/bin/sh", "-c" , "alembic upgrade head && python main.py"]