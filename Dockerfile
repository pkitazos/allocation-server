FROM python:3.9

RUN apt-get update && apt-get install -y \
    coinor-cbc glpk-utils \  # Install CBC and GLPK solvers \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

RUN adduser --disabled-password --gecos "" myuser
USER myuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
