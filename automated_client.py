import socket
import json
import random
import threading
import time
from shared_logic import HOST, PORT

def generate_random_op():
    tipo = random.choice(["soma", "subtracao", "multiplicacao"])
    valores = [random.randint(1, 100) for _ in range(random.randint(2, 5))]
    return {"tipo": tipo, "valores": valores}

def send_request():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        req = {"operacoes": [generate_random_op()]}
        s.send(json.dumps(req).encode())
        s.recv(4096)
        s.close()
    except Exception:
        pass

def run_sequential(n):
    for _ in range(n):
        send_request()

def run_parallel(n):
    threads = []
    for _ in range(n):
        t = threading.Thread(target=send_request)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        sys.exit(1)
        
    mode = sys.argv[1]
    count = int(sys.argv[2])
    
    start = time.time()
    if mode == "st":
        run_sequential(count)
    elif mode == "mt":
        run_parallel(count)
    
    print(f"Tempo total ({mode}): {time.time() - start:.4f}s")
