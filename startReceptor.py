#!/usr/bin/python3
import atexit
import subprocess
import time
import receptor

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
time.sleep(4)
print("      dump1090 iniciado!")

# Parar dump1090 ao encerrar com Ctrl+C
@atexit.register
def exitHandler():
    print("\nEncerrando...")
    dump1090.terminate()
    receptor.stop()

# Iniciar collector com logs no terminal
print("[3/3] Iniciando Collector...")
print("************************************************************")
print("| Logs em tempo real - pressione Ctrl+C para parar        |")
print("************************************************************")
receptor.start()