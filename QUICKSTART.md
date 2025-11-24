# 🚀 INICIO RÁPIDO - Laboratorio Modbus TCP

## Para Estudiantes: 3 Pasos Simples

### 1️⃣ Acceder al Servidor
```bash
ssh tu-usuario@65.109.226.13
```

### 2️⃣ Iniciar el Laboratorio
```bash
cd /mnt/HC_Volume_102919965/modbus_tcp_lab
./start.sh
```

### 3️⃣ Abrir el Dashboard
En tu navegador: **http://65.109.226.13:1880/ui**

---

## ✅ ¡Eso es Todo!

Deberías ver:
- 📊 **4 Gauges** mostrando temperatura, presión y nivel
- 📈 **Gráficos** en tiempo real
- ⚙️ **Setpoints** del sistema

---

## 🛑 Detener el Laboratorio

```bash
./stop.sh
```

---

## 🔍 Ver Estado del Sistema

```bash
./status.sh
```

---

## 🆘 Problemas Comunes

### Dashboard en blanco
```bash
./stop.sh
./start.sh
# Espera 30 segundos y recarga la página (Ctrl+Shift+R)
```

### Contenedores no inician
```bash
docker-compose ps
docker-compose logs -f
```

### Puerto ocupado
```bash
# Verificar qué usa el puerto
sudo netstat -tulpn | grep -E '1880|5020'
```

---

## 📚 Más Información

- Ver **README.md** para documentación completa
- Ver **ACCESO_NODE_RED.md** para detalles del dashboard
- Comandos Docker: `docker-compose --help`

---

## 🎓 Accesos Rápidos

| Qué | Dónde |
|-----|-------|
| **Dashboard** | http://65.109.226.13:1880/ui |
| **Editor** | http://65.109.226.13:1880 |
| **FUXA** | http://65.109.226.13:1881 |
| **Modbus** | 65.109.226.13:5020 |

---

**¿Dudas?** Revisa los logs: `docker-compose logs -f`
