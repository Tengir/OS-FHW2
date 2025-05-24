FROM python:3.12-slim
WORKDIR /app

COPY . .
ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "file_analysis.main:app", "--host", "0.0.0.0", "--port", "8000"]
