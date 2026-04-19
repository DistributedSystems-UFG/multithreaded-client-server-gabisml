import socket
import json
import threading
from shared_logic import HOST, PORT, processar_operacao

def handle_client(conn, addr):
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            requisicao = json.loads(data.decode())
            operacoes = requisicao.get("operacoes", [])
            resultados = []

            for op in operacoes:
                resultado = processar_operacao(op, delay=0.1)
                resultados.append({
                    "operacao": op,
                    "resultado": resultado
                })

            resposta = json.dumps({"resultados": resultados})
            conn.send(resposta.encode())
    except Exception:
        pass
    finally:
        conn.close()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', PORT))
    s.listen(100)

    print(f"Servidor MT pronto na porta {PORT}...")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()

