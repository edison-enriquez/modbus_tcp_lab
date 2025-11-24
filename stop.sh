#!/bin/bash
# Script de detención del Laboratorio Modbus TCP
# Autor: Laboratorio de Sistemas Industriales
# Fecha: Noviembre 2024

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🛑 Deteniendo Laboratorio Modbus TCP..."
echo ""

# Detener contenedores
echo -e "${BLUE}[1/2]${NC} Deteniendo contenedores..."
docker-compose down

echo ""
echo -e "${BLUE}[2/2]${NC} Verificando estado..."
docker-compose ps

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Laboratorio detenido correctamente${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Para volver a iniciar el laboratorio, ejecuta:"
echo -e "${BLUE}$ ./start.sh${NC}"
echo ""
