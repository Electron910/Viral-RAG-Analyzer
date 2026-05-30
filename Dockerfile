# Use Python 3.11 as the base image
FROM python:3.11-slim

# Install system dependencies required for faster-whisper (CTranslate2) and yt-dlp
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the backend requirements and install them
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend code into the container
COPY backend/ .

# Expose port 7860 (Hugging Face Spaces default port)
EXPOSE 7860

# Set environment variable so the app binds to the correct port
ENV PORT=7860

# Command to run the application
CMD ["python", "main.py"]
