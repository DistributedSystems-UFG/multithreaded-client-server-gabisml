from socket import *
from constCS import *
import json
from datetime import datetime

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))


def montar_requisicao():
    operacoes = []

    while True:
        print("\nEscolha uma operação:")
        print("1 - Soma")
        print("2 - Subtração")
        print("3 - Multiplicação")
        print("0 - Enviar requisição")

        op = int(input())

        if op == 0:
            break

        valores = list(map(int, input("Digite números separados por espaço: ").split()))

        if op == 1:
            operacoes.append({"tipo": "soma", "valores": valores})

        elif op == 2:
            operacoes.append({"tipo": "subtracao", "valores": valores})

        elif op == 3:
            operacoes.append({"tipo": "multiplicacao", "valores": valores})

    return {"operacoes": operacoes}


while True:
    req = montar_requisicao()

    if not req["operacoes"]:
        print("Encerrando...")
        break

    t1 = datetime.now()

    s.send(json.dumps(req).encode())
    resposta = s.recv(4096)

    t2 = datetime.now()

    print("\nResposta do servidor:")
    print(json.dumps(json.loads(resposta.decode()), indent=2))

    print(f"Tempo de resposta: {t2 - t1}")

s.close()
