import socket
import time
import threading
import logging

# Configuração
DUMP1090_HOST = "127.0.0.1"
DUMP1090_PORT = 30002

log = logging.getLogger("receptor")

class MicroADSB:
    def __init__(self, device=None, **kwargs):
        self.running = False
        self.onOpen = None
        self.onClose = None
        self.onMessage = None
        self.sock = None

    def open(self):
        self.running = True
        t = threading.Thread(target=self._run)
        t.daemon = True
        t.start()

    def close(self):
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except:
                pass

    def _run(self):
        while self.running:
            try:
                log.info(f"Connecting to dump1090 at {DUMP1090_HOST}:{DUMP1090_PORT}...")
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(60)
                self.sock.connect((DUMP1090_HOST, DUMP1090_PORT))
                
                if self.onOpen: 
                    self.onOpen(None)
                
                buffer = b""
                while self.running:
                    try:
                        data = self.sock.recv(4096)
                        if not data: break
                        
                        buffer += data
                        while b"\n" in buffer:
                            line, buffer = buffer.split(b"\n", 1)
                            line = line.strip()
                            if not line: continue
                            
                            # Formato AVR: *8FE4...;
                            if line.startswith(b"*") and line.endswith(b";"):
                                try:
                                    # String completa (*...;)
                                    full_frame = line.decode('ascii')
                                    # Apenas os dados Hex (sem * e ;) para calculos
                                    hex_data = full_frame[1:-1]
                                    
                                    timestamp_ms = int(time.time() * 1000)
                                    dl_format = (int(hex_data[:2], 16) & 0xF8) >> 3
                                    
                                    raw_obj = {
                                        "timestamp": {"integer": timestamp_ms},
                                        "downlinkformat": dl_format,
                                        # AQUI ESTA O TRUQUE: Enviar a string formatada
                                        "frame": full_frame 
                                    }
                                    
                                    if self.onMessage:
                                        self.onMessage(raw_obj)
                                except Exception as e:
                                    log.error(f"Parse error: {e}")

                    except socket.timeout:
                        continue
                    except Exception as e:
                        raise e

            except Exception as e:
                log.error(f"Connection error: {e}")
                if self.onOpen: self.onOpen(e)
                time.sleep(5)
            finally:
                if self.sock: 
                    self.sock.close()
        
        if self.onClose: 
            self.onClose(None)