FROM python:3.10.6-slim-buster
WORKDIR /app
COPY . .
RUN pip install --upgrade pip setuptools && pip install -r requirements.txt
EXPOSE 8050
WORKDIR /app/ash
CMD ["python", "app.py"]