FROM python:3.14-slim

WORKDIR /app

# Copy requirements first for better caching
COPY src/fetch_meteoswiss_data/requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy database models
COPY database/__init__.py /app/database/__init__.py
COPY database/models.py /app/database/models.py

# Copy application code
COPY src/fetch_meteoswiss_data/*.py /app/fetch_meteoswiss_data/
COPY src/fetch_meteoswiss_data/utils/ /app/fetch_meteoswiss_data/utils/

# Set Python path
ENV PYTHONPATH=/app

WORKDIR /app/fetch_meteoswiss_data

# Run the scheduler
CMD ["python", "scheduler.py"]
