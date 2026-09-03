FROM python:3.14-slim

WORKDIR /app

# Copy requirements first for better caching
COPY src/climate_advisor/requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy database models
COPY database/__init__.py /app/database/__init__.py
COPY database/models.py /app/database/models.py

# Copy application code
COPY src/climate_advisor/*.py /app/climate_advisor/
COPY src/climate_advisor/utils/ /app/climate_advisor/utils/

# Set Python path
ENV PYTHONPATH=/app

WORKDIR /app/climate_advisor

# Run the scheduler
CMD ["python", "scheduler.py"]
