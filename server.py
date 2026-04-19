from socket import *
from constCS import *
import json

def processar_operacao(op):
    tipo = op.get("tipo")
    valores = op.get("valores", [])

    if tipo == "soma":
        return sum(valores)

    elif tipo == "subtracao":
        if not valores:
            return 0
        resultado = valores[0]
        for v in valores[1:]:
            resultado -= v
        return resultado

    elif tipo == "multiplicacao":
        resultado = 1
        for v in valores:
            resultado *= v
        return resultado

    else:
        return f"Operação desconhecida: {tipo}"


s = socket(AF_INET, SOCK_STREAM)
s.bind(('0.0.0.0', PORT))
s.listen(1)

print("Servidor aguardando conexão...")
conn, addr = s.accept()
print(f"Conectado a {addr}")

while True:
    data = conn.recv(4096)

    if not data:
        print("Cliente desconectado")
        break

    try:
        requisicao = json.loads(data.decode())
        operacoes = requisicao.get("operacoes", [])

        resultados = []

        for op in operacoes:
            resultado = processar_operacao(op)
            resultados.append({
                "operacao": op,
                "resultado": resultado
            })

        resposta = json.dumps({"resultados": resultados})
        conn.send(resposta.encode())

    except Exception as e:
        erro = json.dumps({"erro": str(e)})
        conn.send(erro.encode())

conn.close()
