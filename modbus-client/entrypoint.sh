#!/bin/bash

echo "==================================="
echo "Cliente Modbus TCP - Iniciando..."
echo "==================================="

# Esperar a que el servidor esté disponible
echo "Esperando servidor Modbus..."
sleep 10

# Ejecutar el cliente
python -u modbus_client.py
