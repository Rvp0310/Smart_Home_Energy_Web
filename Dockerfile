# Use Python 3.11.9 slim image
FROM python:3.11.9-slim

# Set working directory to the repo root
WORKDIR /app

# Copy everything from repo root into container
COPY . /app

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask default port
EXPOSE 5000

# Run your app
CMD ["python", "app.py"]
