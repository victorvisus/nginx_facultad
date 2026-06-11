FROM python:3.12-slim

WORKDIR /app

# Instalar librerías mínimas del sistema para compilar conectores de BD si fuera necesario
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar los paquetes de tu entorno
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo tu proyecto (incluyendo BBDD, templates y main_facultad_3.py)
COPY . .

# Exponer el puerto de la API
EXPOSE 8000

# Comando estricto para ejecutar tu app con Uvicorn
CMD ["uvicorn", "main_facultad_3:app", "--host", "0.0.0.0", "--port", "8000"]