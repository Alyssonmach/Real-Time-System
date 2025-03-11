import threading
import time
import random
from queue import Queue

# Criando o buffer (Queue já é thread-safe)
buffer_size = 5
buffer = Queue(maxsize = buffer_size)

# Variável de controle para execução
executando = True

# Função do produtor
def produtor():
    while executando:
        item = random.randint(1, 100)  # Produz um item aleatório
        
        buffer.put(item)  # Insere o item na fila (bloqueia se cheia)
        print(f"🟢 Produzido: {item} | Buffer: {list(buffer.queue)}")
        
        time.sleep(random.uniform(0.5, 2))  # Simula tempo de produção

# Função do consumidor
def consumidor():
    while executando or not buffer.empty():  # Continua até o buffer esvaziar
        try:
            item = buffer.get(timeout=1)  # Aguarda um item (timeout evita bloqueio eterno)
            print(f"🔴 Consumido: {item} | Buffer: {list(buffer.queue)}")
            buffer.task_done()  # Marca item como processado
            time.sleep(random.uniform(1, 3))  # Simula tempo de consumo
        except:
            pass  # Se o buffer estiver vazio e `executando` for False, sai do loop

# Função para parar a execução após um tempo
def parar_execucao():
    global executando
    executando = False
    print("\n⏳ Tempo limite atingido! Encerrando...")

# Criando e iniciando as threads
t1 = threading.Thread(target=produtor)
t2 = threading.Thread(target=consumidor)

t1.start()
t2.start()

# Definir tempo limite (ex: 10 segundos)
tempo_limite = 10
timer = threading.Timer(tempo_limite, parar_execucao)
timer.start()

# Aguardar as threads finalizarem
t1.join()
t2.join()

print("🏁 Execução finalizada.")
