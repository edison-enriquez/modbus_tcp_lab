#!/usr/bin/env python3
"""
Monitor continuo de dispositivos Modbus
Genera reportes y alertas
"""

import logging
import time
import schedule
from datetime import datetime
from modbus_client import ModbusClientDevice
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

def monitor_task():
    """Tarea de monitoreo programada"""
    server = os.getenv('MODBUS_SERVER', 'modbus-server')
    port = int(os.getenv('MODBUS_PORT', 502))
    
    client = ModbusClientDevice(server, port)
    
    if client.connect():
        # Leer temperatura
        temp_data = client.read_input_registers(0, 2)
        if temp_data:
            temp1 = temp_data[0] / 100
            temp2 = temp_data[1] / 100
            
            # Verificar alertas de temperatura
            if temp1 > 30.0 or temp2 > 30.0:
                log.warning(f"⚠️  ALERTA: Temperatura elevada! T1={temp1}°C, T2={temp2}°C")
        
        client.disconnect()

if __name__ == "__main__":
    log.info("Monitor de alertas iniciado")
    
    # Programar monitoreo cada 30 segundos
    schedule.every(30).seconds.do(monitor_task)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
