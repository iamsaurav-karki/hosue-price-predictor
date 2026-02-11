FROM python:3.11-slim
WORKDIR /app
# Install dependencies
COPY src/api .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the trained model files into the container
COPY models/trained/*.pkl /app/models/trained/

# Expose the port for the API and Prometheus metrics
EXPOSE 8000 8001

# Command to run the API, using uvicorn as the ASGI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

