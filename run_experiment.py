import subprocess
import time
import os
import signal

def run_test(server_script, client_mode, count):
    print(f"Testando: Server={server_script}, Modo={client_mode}")
    proc = subprocess.Popen(["python3", server_script])
    time.sleep(1)
    
    try:
        out = subprocess.check_output(["python3", "automated_client.py", client_mode, str(count)]).decode()
        print(out.strip())
        return out
    finally:
        os.kill(proc.pid, signal.SIGTERM)
        proc.wait()

def main():
    count = 50
    results = []
    
    results.append(("ST Server / ST Client", run_test("st_server.py", "st", count)))
    results.append(("MT Server / ST Client", run_test("mt_server.py", "st", count)))
    results.append(("MT Server / MT Client", run_test("mt_server.py", "mt", count)))
    
    print("\nRESUMO:")
    for name, res in results:
        print(f"{name}: {res.strip() if res else 'ERRO'}")

if __name__ == "__main__":
    main()
