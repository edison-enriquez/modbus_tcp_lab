#!/usr/bin/env python3
"""
Cliente Modbus TCP
Lee y escribe registros del servidor Modbus
"""

import logging
import time
import os
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

class ModbusClientDevice:
    def __init__(self, host='modbus-server', port=502):
        self.host = host
        self.port = port
        self.client = None
        
    def connect(self):
        """Conectar al servidor Modbus"""
        try:
            self.client = ModbusTcpClient(self.host, port=self.port)
            if self.client.connect():
                log.info(f"✓ Conectado al servidor Modbus {self.host}:{self.port}")
                return True
            else:
                log.error(f"✗ No se pudo conectar a {self.host}:{self.port}")
                return False
        except Exception as e:
            log.error(f"Error de conexión: {e}")
            return False
    
    def disconnect(self):
        """Desconectar del servidor"""
        if self.client:
            self.client.close()
            log.info("Desconectado del servidor Modbus")
    
    def read_holding_registers(self, address, count=1, unit=1):
        """Leer registros de retención (holding registers)"""
        try:
            result = self.client.read_holding_registers(address, count, unit=unit)
            if not result.isError():
                return result.registers
            else:
                log.error(f"Error leyendo registros: {result}")
                return None
        except ModbusException as e:
            log.error(f"Excepción Modbus: {e}")
            return None
    
    def read_input_registers(self, address, count=1, unit=1):
        """Leer registros de entrada (input registers)"""
        try:
            result = self.client.read_input_registers(address, count, unit=unit)
            if not result.isError():
                return result.registers
            else:
                log.error(f"Error leyendo registros de entrada: {result}")
                return None
        except ModbusException as e:
            log.error(f"Excepción Modbus: {e}")
            return None
    
    def write_register(self, address, value, unit=1):
        """Escribir un registro"""
        try:
            result = self.client.write_register(address, value, unit=unit)
            if not result.isError():
                log.info(f"✓ Registro {address} escrito con valor {value}")
                return True
            else:
                log.error(f"Error escribiendo registro: {result}")
                return False
        except ModbusException as e:
            log.error(f"Excepción Modbus: {e}")
            return False
    
    def read_coils(self, address, count=1, unit=1):
        """Leer coils (bobinas)"""
        try:
            result = self.client.read_coils(address, count, unit=unit)
            if not result.isError():
                return result.bits
            else:
                log.error(f"Error leyendo coils: {result}")
                return None
        except ModbusException as e:
            log.error(f"Excepción Modbus: {e}")
            return None
    
    def write_coil(self, address, value, unit=1):
        """Escribir un coil"""
        try:
            result = self.client.write_coil(address, value, unit=unit)
            if not result.isError():
                log.info(f"✓ Coil {address} escrito con valor {value}")
                return True
            else:
                log.error(f"Error escribiendo coil: {result}")
                return False
        except ModbusException as e:
            log.error(f"Excepción Modbus: {e}")
            return False

def main():
    """Función principal del cliente"""
    server = os.getenv('MODBUS_SERVER', 'modbus-server')
    port = int(os.getenv('MODBUS_PORT', 502))
    
    log.info("="*60)
    log.info("Cliente Modbus TCP - Dispositivo de Monitoreo")
    log.info("="*60)
    
    client = ModbusClientDevice(server, port)
    
    # Intentar conectar con reintentos
    retries = 5
    while retries > 0:
        if client.connect():
            break
        log.warning(f"Reintentando conexión... ({retries} intentos restantes)")
        time.sleep(5)
        retries -= 1
    
    if not client.client.is_socket_open():
        log.error("No se pudo establecer conexión. Saliendo...")
        return
    
    try:
        log.info("Iniciando monitoreo de registros...")
        
        while True:
            log.info("-" * 60)
            
            # Leer registros de entrada (sensores)
            input_regs = client.read_input_registers(0, 5)
            if input_regs:
                log.info("📊 SENSORES (Input Registers):")
                log.info(f"  Temperatura 1: {input_regs[0]/100:.1f}°C")
                log.info(f"  Temperatura 2: {input_regs[1]/100:.1f}°C")
                log.info(f"  Presión: {input_regs[2]/100:.1f} bar")
                log.info(f"  Nivel: {input_regs[3]/100:.1f}%")
            
            # Leer registros de retención (configuración)
            holding_regs = client.read_holding_registers(0, 5)
            if holding_regs:
                log.info("⚙️  CONFIGURACIÓN (Holding Registers):")
                log.info(f"  Setpoint Temp: {holding_regs[0]/100:.1f}°C")
                log.info(f"  Setpoint Nivel: {holding_regs[1]/100:.1f}%")
                log.info(f"  Modo: {'AUTO' if holding_regs[3] == 1 else 'MANUAL'}")
            
            # Esperar antes de la siguiente lectura
            time.sleep(10)
            
    except KeyboardInterrupt:
        log.info("\nMonitoreo detenido por el usuario")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
