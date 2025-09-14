# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV KMP_DUPLICATE_LIB_OK=TRUE

# Expose port
EXPOSE 8001

# Change to src directory and run the application
WORKDIR /app/src
CMD ["python", "application.py"]
