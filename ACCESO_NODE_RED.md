# 🎯 Acceso al Dashboard Node-RED

## ✅ Estado Actual

El laboratorio Modbus TCP está **totalmente operativo** con visualización en tiempo real.

### 🌐 URLs de Acceso

#### Node-RED Dashboard (Recomendado)
- **URL Externa**: http://65.109.226.13:1880/ui
- **URL Local**: http://localhost:1880/ui
- **Editor Node-RED**: http://65.109.226.13:1880

#### FUXA SCADA (Disponible pero con errores de driver)
- **URL Externa**: http://65.109.226.13:1881
- **URL Local**: http://localhost:1881
- **Estado**: Interface carga pero tiene errores en driver Modbus

---

## 📊 Dashboard Node-RED

### Características
- ✅ **4 Gauges de Sensores**: Temperatura 1, Temperatura 2, Presión, Nivel
- ✅ **Gráficas en Tiempo Real**: Temperaturas y Nivel
- ✅ **Visualización de Setpoints**: SP Temperatura, SP Nivel, Tiempo Ciclo, Modo
- ✅ **Actualización cada 2 segundos**
- ✅ **Tema oscuro moderno**

### Variables Visualizadas

#### Input Registers (Sensores)
| Variable | Dirección Modbus | Valor Actual | Unidad | Rango |
|----------|------------------|--------------|--------|-------|
| Temperatura 1 | IR0 (30001) | 25.5 | °C | 0-50 |
| Temperatura 2 | IR1 (30002) | 30.0 | °C | 0-50 |
| Presión | IR2 (30003) | 15.0 | bar | 0-30 |
| Nivel Tanque | IR3 (30004) | 75.0 | % | 0-100 |

#### Holding Registers (Setpoints)
| Variable | Dirección Modbus | Valor Actual | Unidad |
|----------|------------------|--------------|--------|
| Setpoint Temp | HR0 (40001) | 20.0 | °C |
| Setpoint Nivel | HR1 (40002) | 50.0 | % |
| Tiempo Ciclo | HR2 (40003) | 100 | ms |
| Modo Operación | HR3 (40004) | AUTO | - |

---

## 🔧 Configuración Técnica

### Conexión Modbus
- **Servidor Modbus**: 172.25.0.10:502
- **Protocolo**: Modbus TCP
- **Unit ID**: 1
- **Tipo de lectura**: 
  - Input Registers: FC4 (Read Input Registers)
  - Holding Registers: FC3 (Read Holding Registers)

### Nodos Instalados
```bash
node-red-contrib-modbus  # Comunicación Modbus TCP
node-red-dashboard       # Dashboard web v3.6.6
```

---

## 🚀 Instrucciones de Uso

### 1. Acceder al Dashboard
```bash
# Desde tu navegador:
http://65.109.226.13:1880/ui
```

### 2. Editar el Flujo (Opcional)
```bash
# Editor Node-RED:
http://65.109.226.13:1880
```

### 3. Verificar Conectividad
```bash
# Ver logs de Node-RED:
docker logs -f nodered

# Ver logs del servidor Modbus:
docker logs -f modbus-tcp-server

# Ver logs del cliente de monitoreo:
docker-compose logs -f modbus-client-device
```

---

## 🛠️ Comandos Útiles

### Gestión de Contenedores
```bash
cd /mnt/HC_Volume_102919965/modbus_tcp_lab

# Ver estado
docker-compose ps

# Reiniciar Node-RED
docker-compose restart nodered

# Reiniciar todo el laboratorio
docker-compose restart

# Ver logs en tiempo real
docker-compose logs -f nodered
```

### Modificar el Flujo
1. Accede al editor: http://65.109.226.13:1880
2. Realiza cambios en el flujo
3. Click en "Deploy" (esquina superior derecha)
4. El dashboard se actualiza automáticamente

---

## 📁 Estructura del Proyecto

```
/mnt/HC_Volume_102919965/modbus_tcp_lab/
├── docker-compose.yml          # Orquestación de contenedores
├── modbus-server/
│   ├── modbus_server.py       # Servidor Modbus TCP
│   └── config.json            # Configuración del servidor
├── modbus-client/
│   ├── modbus_client.py       # Cliente de monitoreo
│   └── monitor.py             # Script de lectura
├── scada-hmi/
│   └── data/project.fuxap.db  # Base de datos FUXA
├── nodered/
│   └── data/flows.json        # Flujos de Node-RED
└── README.md                   # Documentación principal
```

---

## 🌐 Red Docker

```
Nombre: modbus_network
Subnet: 172.25.0.0/24

Contenedores:
├── modbus-tcp-server      → 172.25.0.10:502 (puerto host: 5020)
├── modbus-client-device   → 172.25.0.11
├── scada-hmi (FUXA)       → 172.25.0.20:1881 (puerto host: 1881)
└── nodered                → 172.25.0.21:1880 (puerto host: 1880)
```

---

## 🔍 Troubleshooting

### Dashboard Vacío
Si el dashboard aparece vacío:
```bash
# 1. Verificar que el servidor Modbus esté corriendo
docker logs modbus-tcp-server

# 2. Reiniciar Node-RED
docker-compose restart nodered

# 3. Limpiar caché del navegador (Ctrl+Shift+R)
```

### Sin Datos
Si no aparecen datos en los gauges:
```bash
# Verificar conectividad Modbus
docker logs nodered | grep -i modbus

# Verificar que el cliente puede leer
docker-compose logs modbus-client-device | tail -20
```

### Error de Conexión
```bash
# Verificar que todos los contenedores estén UP
docker-compose ps

# Revisar la red Docker
docker network inspect modbus_network
```

---

## 📌 Notas Importantes

1. **Acceso Remoto**: El servidor está accesible desde `65.109.226.13`
2. **FUXA**: Tiene problemas con el driver Modbus, se recomienda usar Node-RED
3. **Persistencia**: Los datos del dashboard Node-RED se pierden al reiniciar (solo visualización en tiempo real)
4. **Seguridad**: No hay autenticación configurada, acceso abierto en puertos 1880 y 1881

---

## 🎓 Próximos Pasos Sugeridos

### 1. Análisis de Tráfico
Sin Kali Linux disponible (removido por espacio), puedes usar:
```bash
# tcpdump en el host
sudo tcpdump -i any port 502 -w modbus_capture.pcap

# Analizar con tshark
tshark -r modbus_capture.pcap -Y "modbus"
```

### 2. Escribir Valores Modbus
Puedes agregar nodos de escritura en Node-RED:
- `modbus-write`: Para escribir Holding Registers
- `ui_slider`: Para controlar setpoints desde el dashboard

### 3. Alarmas y Notificaciones
Agregar nodos de:
- Comparación de valores
- Notificaciones por email
- Alertas visuales en dashboard

---

## ✅ Verificación Final

Estado de servicios:
- ✅ Servidor Modbus TCP: OPERATIVO (172.25.0.10:502)
- ✅ Cliente de Monitoreo: OPERATIVO (leyendo cada 10s)
- ✅ Node-RED Dashboard: OPERATIVO (http://65.109.226.13:1880/ui)
- ⚠️ FUXA SCADA: PARCIAL (interfaz carga, driver con errores)

**Última actualización**: 24 de Noviembre 2024
