import threading
import time
import random
from queue import Queue

# Criando o buffer (Queue já é thread-safe)
buffer_size = 5
buffer = Queue(maxsize=buffer_size)  # Define o tamanho do buffer

# Função do produtor
def produtor():
    while True:
        item = random.randint(1, 100)  # Produz um item aleatório
        
        buffer.put(item)  # Insere o item na fila (bloqueia se estiver cheia)
        print(f"🟢 Produzido: {item} | Buffer: {list(buffer.queue)}")
        
        time.sleep(random.uniform(0.5, 2))  # Simula tempo de produção

# Função do consumidor
def consumidor():
    while True:
        item = buffer.get()  # Remove um item da fila (bloqueia se estiver vazia)
        print(f"🔴 Consumido: {item} | Buffer: {list(buffer.queue)}")
        
        time.sleep(random.uniform(1, 3))  # Simula tempo de consumo
        buffer.task_done()  # Indica que o processamento do item foi concluído

# Criando as threads
t1 = threading.Thread(target=produtor)
t2 = threading.Thread(target=consumidor)

# Iniciando as threads
t1.start()
t2.start()

# Mantém a execução indefinidamente
t1.join()
t2.join()
