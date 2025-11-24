FROM python:3.11-slim

LABEL maintainer="Modbus TCP Lab"
LABEL description="Servidor Modbus TCP simulando un PLC/Dispositivo Industrial"

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar pymodbus
RUN pip install --no-cache-dir pymodbus==3.6.4

# Crear directorio de trabajo
WORKDIR /app

# Copiar scripts
COPY modbus_server.py .
COPY config.json .

# Exponer puerto Modbus TCP (502)
EXPOSE 502

# Ejecutar el servidor
CMD ["python", "-u", "modbus_server.py"]
