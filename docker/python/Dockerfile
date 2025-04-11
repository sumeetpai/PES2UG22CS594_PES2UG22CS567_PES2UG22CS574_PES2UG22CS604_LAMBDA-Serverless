FROM python:3.9-slim

WORKDIR /app

# Install required packages
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    sqlalchemy \
    pymysql \
    python-dotenv

# Copy the run script
COPY ./run.py /app/

# Set the entrypoint
ENTRYPOINT ["python", "/app/run.py"] 