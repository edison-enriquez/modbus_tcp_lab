#!/bin/bash
# Script de inicio del Laboratorio Modbus TCP
# Autor: Laboratorio de Sistemas Industriales
# Fecha: Noviembre 2024

set -e

echo "🏭 Iniciando Laboratorio Modbus TCP..."
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Verificar Docker
echo -e "${BLUE}[1/5]${NC} Verificando Docker..."
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker no está instalado${NC}"
    exit 1
fi
if ! docker info &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker no está corriendo${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Docker OK"
echo ""

# 2. Verificar Docker Compose
echo -e "${BLUE}[2/5]${NC} Verificando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker Compose no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Docker Compose OK"
echo ""

# 3. Detener contenedores previos si existen
echo -e "${BLUE}[3/5]${NC} Limpiando contenedores previos..."
docker-compose down 2>/dev/null || true
echo -e "${GREEN}✓${NC} Limpieza completa"
echo ""

# 4. Iniciar servicios
echo -e "${BLUE}[4/5]${NC} Iniciando servicios..."
docker-compose up -d
echo -e "${GREEN}✓${NC} Servicios iniciados"
echo ""

# 5. Esperar a que los servicios estén listos
echo -e "${BLUE}[5/5]${NC} Esperando a que los servicios estén listos..."
echo "   Esto puede tomar ~30 segundos..."
sleep 15

# Verificar estado
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Laboratorio Modbus TCP iniciado correctamente${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Mostrar estado de los contenedores
docker-compose ps
echo ""

# Obtener IP del servidor
SERVER_IP="65.109.226.13"

# Mostrar URLs de acceso
echo "📊 ACCESO A LAS INTERFACES:"
echo ""
echo -e "   ${GREEN}Node-RED Dashboard:${NC}"
echo -e "   🌐 http://${SERVER_IP}:1880/ui"
echo -e "   📱 http://localhost:1880/ui (local)"
echo ""
echo -e "   ${BLUE}Editor Node-RED:${NC}"
echo -e "   🛠️  http://${SERVER_IP}:1880"
echo ""
echo -e "   ${YELLOW}FUXA SCADA:${NC}"
echo -e "   ⚠️  http://${SERVER_IP}:1881"
echo ""
echo -e "   ${GREEN}Servidor Modbus TCP:${NC}"
echo -e "   🔌 ${SERVER_IP}:5020"
echo ""

# Mostrar comandos útiles
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 COMANDOS ÚTILES:"
echo ""
echo "   Ver logs en tiempo real:"
echo "   $ docker-compose logs -f"
echo ""
echo "   Ver estado de contenedores:"
echo "   $ docker-compose ps"
echo ""
echo "   Detener laboratorio:"
echo "   $ ./stop.sh"
echo ""
echo "   Reiniciar un servicio:"
echo "   $ docker-compose restart nodered"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}🎓 ¡Listo para comenzar!${NC}"
echo ""

# Esperar a que Node-RED esté completamente listo
echo "⏳ Esperando a que Node-RED esté completamente listo..."
sleep 15

# Verificar que Node-RED responde
if curl -s http://localhost:1880/ui > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Node-RED Dashboard listo"
else
    echo -e "${YELLOW}⚠️${NC}  Node-RED aún está iniciando, espera unos segundos más"
fi

echo ""
echo -e "${BLUE}💡 Tip:${NC} Abre http://${SERVER_IP}:1880/ui en tu navegador"
echo ""
