import threading
import time
import random

# Buffer compartilhado
buffer = list()
buffer_size = 5 # tamanho máximo do buffer

# Semáforos
empty = threading.Semaphore(buffer_size) # Controla espaços vazios
full = threading.Semaphore(0) # Controla itens disponíveis
mutex = threading.Semaphore(1) # Exclusão mútua

# Função do produtor
def produtor():
    while True:
        item = random.randint(1, 100) # Produz um item aleatório

        empty.acquire() # Espera espaço disponível no buffer
        mutex.acquire() # Garante exclusão mútua

        buffer.append(item)
        print(f"🟢 Produzido: {item} | Buffer: {buffer}")

        mutex.release()  # Libera exclusão mútua
        full.release()   # Indica que há um item disponível

        time.sleep(random.uniform(0.5, 2))  # Simula tempo de produção

# Função do consumidor
def consumidor():
    while True:
        full.acquire()  # Espera um item disponível no buffer
        mutex.acquire() # Garante exclusão mútua
        
        item = buffer.pop(0)  # Consome um item
        print(f"🔴 Consumido: {item} | Buffer: {buffer}")
        
        mutex.release() # Libera exclusão mútua
        empty.release() # Indica que há espaço disponível
        
        time.sleep(random.uniform(1, 3))  # Simula tempo de consumo

# Criando as threads
t1 = threading.Thread(target=produtor)
t2 = threading.Thread(target=consumidor)

# Iniciando as threads
t1.start()
t2.start()

# Mantém a execução indefinidamente
t1.join()
t2.join()

