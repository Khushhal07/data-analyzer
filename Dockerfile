FROM python:3.11-slim

WORKDIR /app

# Fast mirror & pre-compiled binary wheels only (no slow compiling)
COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary=:all: -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
