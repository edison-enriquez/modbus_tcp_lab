#!/usr/bin/env python3
import logging
import json
from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification  
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        log.warning(f"Config error: {e}")
        return {"host": "0.0.0.0", "port": 502, "device_info": {"vendor": "ModbusLab", "product_code": "PLC-001", "version": "1.0", "vendor_url": "http://modbus.org", "product_name": "Modbus Simulator", "model_name": "PLC-SIM"}}

def setup_data_blocks():
    coils = ModbusSequentialDataBlock(0, [0] * 100)
    discrete_inputs = ModbusSequentialDataBlock(0, [0] * 100)
    input_registers = ModbusSequentialDataBlock(0, [2550, 3000, 1500, 7500, 0] + [0] * 95)
    holding_registers = ModbusSequentialDataBlock(0, [2000, 5000, 100, 1, 0] + [0] * 95)
    store = ModbusSlaveContext(di=discrete_inputs, co=coils, ir=input_registers, hr=holding_registers, zero_mode=True)
    return ModbusServerContext(slaves=store, single=True)

def setup_device_identity(config):
    identity = ModbusDeviceIdentification()
    identity.VendorName = config['device_info']['vendor']
    identity.ProductCode = config['device_info']['product_code']
    identity.VendorUrl = config['device_info']['vendor_url']
    identity.ProductName = config['device_info']['product_name']
    identity.ModelName = config['device_info']['model_name']
    identity.MajorMinorRevision = config['device_info']['version']
    return identity

def run_server():
    config = load_config()
    log.info("="*60)
    log.info("Servidor Modbus TCP Iniciado")
    log.info(f"Host: {config['host']}:{config['port']}")
    log.info("="*60)
    context = setup_data_blocks()
    identity = setup_device_identity(config)
    StartTcpServer(context=context, identity=identity, address=(config['host'], config['port']))

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        log.info("Server stopped")
    except Exception as e:
        log.error(f"Error: {e}", exc_info=True)
