# Use Python 3.11.9 slim image
FROM python:3.11.9-slim

WORKDIR /app
COPY . /app

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Let Flask listen on whatever PORT Render sets
ENV PORT 10000
EXPOSE $PORT

CMD ["sh", "-c", "python app.py"]
