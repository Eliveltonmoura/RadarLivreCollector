#!/usr/bin/python3
import atexit
import subprocess
import time
import sys
import os

print("************************************************************")
print("| Iniciando RadarLivre Collector                           |")
print("************************************************************")

# Matar instâncias anteriores do dump1090
print("[1/3] Limpando processos anteriores...")
subprocess.call(["sudo", "pkill", "-9", "dump1090-mutability"], stderr=subprocess.DEVNULL)
time.sleep(2)

# Iniciar dump1090 em background
print("[2/3] Iniciando dump1090...")
dump1090 = subprocess.Popen(
    ["sudo", "dump1090-mutability", "--net", "--quiet"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(3)

# Verificar se dump1090 subiu
result = subprocess.call(["pgrep", "-x", "dump1090-mutab"], stdout=subprocess.DEVNULL)
if result != 0:
    print("      ERRO: dump1090 nao iniciou. Verifique o RTL-SDR.")
    sys.exit(1)
else:
    print("      dump1090 OK (RTL-SDR ativo)")

# Parar dump1090 ao encerrar
@atexit.register
def exitHandler():
    print("\nEncerrando...")
    dump1090.terminate()
    receptor.stop()

# Iniciar collector
print("[3/3] Iniciando Collector...")
print("************************************************************")
print("| Logs em tempo real - pressione Ctrl+C para parar        |")
print("************************************************************")

import receptor
receptor.start()