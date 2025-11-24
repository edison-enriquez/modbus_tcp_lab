#!/usr/bin/env python3
"""
Generador de diagramas para el Laboratorio Modbus TCP
Usa la librería 'diagrams' para crear diagramas as code
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Nginx
from diagrams.onprem.monitoring import Grafana
from diagrams.programming.language import Python
from diagrams.generic.compute import Rack
from diagrams.generic.network import Switch
from diagrams.generic.storage import Storage
from diagrams.custom import Custom
import os

# Configuración de diagramas
graph_attr = {
    "fontsize": "14",
    "bgcolor": "white",
    "pad": "0.5"
}

node_attr = {
    "fontsize": "12",
    "height": "1.5",
    "width": "2"
}

# Diagrama 1: Arquitectura del Sistema
with Diagram("Arquitectura Laboratorio Modbus TCP", 
             filename="docs/arquitectura_modbus",
             show=False,
             direction="TB",
             graph_attr=graph_attr,
             node_attr=node_attr):
    
    with Cluster("Acceso Externo"):
        user = Grafana("Usuario\n65.109.226.13")
    
    with Cluster("Red Docker: modbus_network\n172.25.0.0/24"):
        
        with Cluster("Servidor PLC"):
            modbus_server = Python("Modbus Server\n172.25.0.10:502\nPuerto: 5020")
        
        with Cluster("Interfaces Visualización"):
            nodered = Grafana("Node-RED Dashboard\n172.25.0.21:1880\nPuerto: 1880")
            fuxa = Nginx("FUXA SCADA\n172.25.0.20:1881\nPuerto: 1881")
        
        with Cluster("Monitoreo"):
            client = Python("Modbus Client\n172.25.0.11\nLee cada 10s")
    
    # Conexiones
    user >> Edge(label="HTTP :1880/ui", color="green", style="bold") >> nodered
    user >> Edge(label="HTTP :1881", color="orange") >> fuxa
    user >> Edge(label="Modbus :5020", color="red") >> modbus_server
    
    modbus_server >> Edge(label="Modbus TCP\nFC3/FC4", color="darkgreen") >> nodered
    modbus_server >> Edge(label="Modbus TCP", color="orange") >> fuxa
    modbus_server >> Edge(label="Modbus TCP\nPolling", color="blue") >> client

# Diagrama 2: Variables Modbus
with Diagram("Variables Modbus - Input Registers",
             filename="docs/variables_input_registers",
             show=False,
             direction="LR",
             graph_attr=graph_attr,
             node_attr=node_attr):
    
    with Cluster("Input Registers - FC4 (Solo Lectura)"):
        ir0 = Storage("IR0: 30001\nTemperatura 1\n25.5°C")
        ir1 = Storage("IR1: 30002\nTemperatura 2\n30.0°C")
        ir2 = Storage("IR2: 30003\nPresión\n15.0 bar")
        ir3 = Storage("IR3: 30004\nNivel Tanque\n75.0%")

with Diagram("Variables Modbus - Holding Registers",
             filename="docs/variables_holding_registers",
             show=False,
             direction="LR",
             graph_attr=graph_attr,
             node_attr=node_attr):
    
    with Cluster("Holding Registers - FC3/FC6/FC16 (R/W)"):
        hr0 = Rack("HR0: 40001\nSP Temperatura\n20.0°C")
        hr1 = Rack("HR1: 40002\nSP Nivel\n50.0%")
        hr2 = Rack("HR2: 40003\nTiempo Ciclo\n100 ms")
        hr3 = Rack("HR3: 40004\nModo\nAUTO")

print("✅ Diagramas generados exitosamente en docs/")
print("   - arquitectura_modbus.png")
print("   - variables_input_registers.png")
print("   - variables_holding_registers.png")
