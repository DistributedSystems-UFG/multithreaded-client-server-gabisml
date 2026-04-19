import socket
import json
from shared_logic import PORT, processar_operacao

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', PORT))
    s.listen(5)

    print(f"Servidor ST pronto na porta {PORT}...")

    while True:
        conn, addr = s.accept()
        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                req = json.loads(data.decode())
                resultados = []
                for op in req.get("operacoes", []):
                    res = processar_operacao(op, delay=0.1)
                    resultados.append({"operacao": op, "resultado": res})
                conn.send(json.dumps({"resultados": resultados}).encode())
        except Exception:
            pass
        finally:
            conn.close()

if __name__ == "__main__":
    start_server()
