FROM python:3.11.5

COPY src/requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

EXPOSE 8080
ENTRYPOINT ["/bin/sh", "-c" , "alembic upgrade head && python main.py"]