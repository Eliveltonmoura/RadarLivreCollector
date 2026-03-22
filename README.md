# 📡 RadarLivre Collector

> Collector ADS-B rodando no Banana Pi M4 Berry com RTL-SDR

---

## ℹ️ Informações

| Item | Valor |
|------|-------|
| Dispositivo | Banana Pi M4 Berry — Armbian 24.8.2 Jammy (ARM64) |
| Receptor ADS-B | RTL2838UHIDIR (Realtek R820T) |


---

## ⚙️ Pré-requisitos

- Banana Pi com Armbian/Ubuntu
- RTL-SDR conectado via USB
- Servidor RadarLivre rodando e acessível na rede
- Python 3

---

## 📦 Instalação

```bash
git clone https://github.com/Eliveltonmoura/RadarLivreCollector.git
cd RadarLivreCollector
sudo bash INSTALL.sh
```

---

## 🔧 Configuração

Edite o arquivo `config.py`:

```bash
cat > config.py << 'EOF'
SERVER_HOST = "IP_DO_SERVIDOR:8000"
LOGIN = "seu_usuario"
PASSWORD = "sua_senha"
COLLECTOR_ID = "seu-collector-id"
DATABASE_DIR = "data"
LOG_DIR = "log"
COLLECTOR_ADDRESS = '/dev/ttyACM0'
MAX_MESSAGE_AGE = 60 * 1000
DATA_OUTPUT_ENABLED = False
DATA_OUTPUT_HOST = "127.0.0.1"
DATA_OUTPUT_PORT = 30003
LOCAL_DATA_ENABLED = False
EOF
```

> ⚠️ O Collector ID é gerado no servidor com o comando:
> ```bash
> sudo docker exec -it radar_livre python manage.py createcollector <usuario> <lat> <lon>
> ```

---

## ▶️ Executar

### 1. Iniciar o dump1090 (captura de sinais do RTL-SDR)

```bash
sudo nohup dump1090-mutability --net --quiet > /dev/null 2>&1 &
```

### 2. Iniciar o Collector

```bash
sudo nohup python3 startReceptor.py > /tmp/collector.log 2>&1 &
```

### 3. Monitorar logs

```bash
tail -f /tmp/collector.log
```

Saída esperada:
```
INFO:receptor:Starting receptor...
INFO:receptor:Receptor open: opened!
DEBUG:urllib3... "PUT /api/collector/...
```

---

## 🔄 Reiniciar após Reboot

```bash
sudo nohup dump1090-mutability --net --quiet > /dev/null 2>&1 &
sudo nohup python3 ~/RadarLivreCollector/startReceptor.py > /tmp/collector.log 2>&1 &
```

---

## ✅ Verificação

| Componente | Comando |
|------------|---------|
| RTL-SDR detectado | `lsusb \| grep -i realtek` |
| dump1090 rodando | `ps aux \| grep dump1090` |
| Porta 30002 aberta | `ss -tlnp \| grep 30002` |
| Logs do collector | `tail /tmp/collector.log` |

---

## 🛠️ Problemas Comuns

### RTL-SDR ocupado (`Device or resource busy`)

```bash
sudo pkill -9 dump1090-mutability
sleep 3
sudo nohup dump1090-mutability --net --quiet > /dev/null 2>&1 &
```

### Processo suspenso (estado `T`)

```bash
ps aux | grep dump1090   # anotar o PID
sudo kill -9 <PID>
sleep 3
sudo nohup dump1090-mutability --net --quiet > /dev/null 2>&1 &
```

### Collector não conecta ao servidor

Verifique o `config.py`:
```bash
cat config.py
```
Confirme que `SERVER_HOST` aponta para o IP correto do servidor.

---
elivelton Moura

## 🔗 Repositório do Servidor

https://github.com/RadarLivre/RadarLivre