
from residentes import simulacao_residentes
from elevador import simulacao_elevador
import threading
import random
import time

residentes = ['Celinha', 'Mário', 'Rita', 'Arnaldo', 'Isadora', 'Álvara', 'Bozena',
             'Tatalo', 'Copellia', 'Deise', 'Ladir']
andar_inicial = 0
max_andar = 5

pessoas = simulacao_residentes(nome_residentes = residentes)
gestao_elevador = simulacao_elevador(andar_inicial = andar_inicial)

dim_lista_compartilhada = max_andar * 2

chamadas_por_andar = [list()] * max_andar
lista_compartilhada = list()


capacidade_maxima_chamados = threading.Semaphore(dim_lista_compartilhada)
mutex = threading.Semaphore(1)

def solicita_elevador():

    while True:

        capacidade_maxima_chamados.acquire()
        mutex.acquire()

        status, dados_usuario = pessoas.inicia_chamada(max_andares = max_andar)
        print(f"Nova Chamada: {dados_usuario['Nome']} ({dados_usuario['Andar Partida']} -> {dados_usuario['Andar Chegada']})")

        if status:
            lista_compartilhada.append(dados_usuario)
        
        mutex.release()
        time.sleep(random.uniform(1, 5))

def verifica_andares():

    while True:

        mutex.acquire()

        for andar in range(1, max_andar + 1):
            chamados = pessoas.get_chamados_por_andar(num_andar = andar)
            chamadas_por_andar[andar -1] = chamados
        
        print('Chamadas por Andar:')
        for index, andar in enumerate(chamadas_por_andar):
            info = list()
            
            for dados_usuario in andar:
                info.append([dados_usuario['Nome'], dados_usuario['Andar Partida'], dados_usuario['Andar Chegada']])
            
            print(f'{index + 1}: {info}')

        mutex.release()
        time.sleep(1)

t1 = threading.Thread(target = solicita_elevador)
t2 = threading.Thread(target = verifica_andares)

t1.start()
t2.start()

t1.join()
t2.join()

