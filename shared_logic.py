import time

HOST = "127.0.0.1"
PORT = 5678

def processar_operacao(op, delay=0.0):
    if delay > 0:
        time.sleep(delay)
        
    tipo = op.get("tipo")
    valores = op.get("valores", [])

    if tipo == "soma":
        return sum(valores)

    elif tipo == "subtracao":
        if not valores: return 0
        res = valores[0]
        for v in valores[1:]: res -= v
        return res

    elif tipo == "multiplicacao":
        res = 1
        for v in valores: res *= v
        return res

    return f"Erro: {tipo}"
