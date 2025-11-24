#!/bin/bash
# Script de verificación del sistema
# Comprueba que todo esté funcionando correctamente

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🔍 Verificando estado del Laboratorio Modbus TCP..."
echo ""

# 1. Verificar contenedores
echo -e "${BLUE}[1/4]${NC} Estado de contenedores:"
docker-compose ps
echo ""

# 2. Verificar conectividad Modbus
echo -e "${BLUE}[2/4]${NC} Verificando servidor Modbus TCP..."
if timeout 3 bash -c "echo > /dev/tcp/172.25.0.10/502" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Servidor Modbus TCP accesible (172.25.0.10:502)"
else
    echo -e "${YELLOW}⚠️${NC}  Servidor Modbus no responde aún"
fi
echo ""

# 3. Verificar Node-RED
echo -e "${BLUE}[3/4]${NC} Verificando Node-RED..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:1880/ui 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ]; then
    echo -e "${GREEN}✓${NC} Node-RED Dashboard accesible (http://localhost:1880/ui)"
else
    echo -e "${YELLOW}⚠️${NC}  Node-RED no responde (código: $HTTP_CODE)"
fi
echo ""

# 4. Verificar FUXA
echo -e "${BLUE}[4/4]${NC} Verificando FUXA..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:1881 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ]; then
    echo -e "${GREEN}✓${NC} FUXA SCADA accesible (http://localhost:1881)"
else
    echo -e "${YELLOW}⚠️${NC}  FUXA no responde (código: $HTTP_CODE)"
fi
echo ""

# Mostrar logs recientes
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📋 Logs recientes del servidor Modbus:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
docker logs modbus-tcp-server 2>&1 | tail -5
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📋 Logs recientes del cliente Modbus:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
docker logs modbus-client-device 2>&1 | tail -5
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Verificación completada${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
