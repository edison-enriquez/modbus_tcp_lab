FROM python:3.11-slim

LABEL maintainer="Modbus TCP Lab"
LABEL description="Cliente Modbus TCP - Dispositivo de monitoreo"

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar pymodbus y otras utilidades
RUN pip install --no-cache-dir \
    pymodbus==3.6.4 \
    schedule

WORKDIR /app

# Copiar scripts
COPY modbus_client.py .
COPY monitor.py .

# Script de entrada
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
