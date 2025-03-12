
from residentes import simulacao_residentes
from elevador import simulacao_elevador
import threading
import random
import time
import os

residentes = ['Celinha', 'Mário', 'Rita', 'Arnaldo', 'Isadora', 'Álvara', 'Bozena',
             'Tatalo', 'Copellia', 'Deise', 'Ladir']
andar_inicial = 0
max_andar = 5

pessoas = simulacao_residentes(nome_residentes = residentes)
gestao_elevador = simulacao_elevador(andar_inicial = andar_inicial)

dim_lista_compartilhada = max_andar * 2

chamadas_por_andar = [list()] * max_andar
lista_compartilhada = list()
chamado_atual = list()


capacidade_maxima_chamados = threading.Semaphore(dim_lista_compartilhada)
elevador_operante = threading.Semaphore(1)
mutex = threading.Semaphore(1)

def solicita_elevador():

    while True:

        capacidade_maxima_chamados.acquire()
        status, dados_usuario = pessoas.inicia_chamada(max_andares = max_andar)

        if status:
            lista_compartilhada.append(dados_usuario)

        time.sleep(random.uniform(4, 7))

def processa_chamado():

    while True:

        if len(lista_compartilhada) != 0:

            elevador_operante.acquire()
            chamado_atual.append(lista_compartilhada.pop(0))

        time.sleep(1)


def move_elevador():

    status_elevador_partida = True
    status_elevador_chegada = not status_elevador_partida
    primeira_interacao = 0
    
    time.sleep(3)

    while True:
        
        if len(chamado_atual) != 0:
            
            while status_elevador_partida:
                if primeira_interacao == 0:
                    gestao_elevador.set_status(1)
                    gestao_elevador.set_chegada(chamado_atual[0]['Andar Partida'])

                time.sleep(0.5)
                status_elevador_partida = gestao_elevador.movimenta_elevador()
                time.sleep(1)
                primeira_interacao += 1

                if status_elevador_partida == False:
                    status_elevador_chegada = True
                    primeira_interacao = 0
            
            while status_elevador_chegada:
                if primeira_interacao == 0:
                    gestao_elevador.set_status(1)
                    gestao_elevador.set_chegada(chamado_atual[0]['Andar Chegada']) 
                    pessoas.set_status(id_residente = chamado_atual[0]['ID'], seleciona_status = 2)

                time.sleep(0.5)
                status_elevador_chegada =  gestao_elevador.movimenta_elevador()
                time.sleep(1)
                primeira_interacao += 1

                if status_elevador_chegada == False:
                    status_elevador_partida = True
                    primeira_interacao = 0

                    pessoas.set_status(id_residente = chamado_atual[0]['ID'], seleciona_status = 0)
                    pessoas.set_andares(id_residente = chamado_atual[0]['ID'], andar_inicial = 0, andar_final = 0)
                    chamado_atual.pop(0)
                    elevador_operante.release()
                    capacidade_maxima_chamados.release()

        
        time.sleep(1)
            
            
def visualiza_lista_por_andar():

    for andar in range(1, max_andar + 1):
        chamados = pessoas.get_chamados_por_andar(num_andar = andar)
        chamadas_por_andar[andar - 1] = chamados

    print(f'=== Chamadas por Andar {len(lista_compartilhada) + len(chamado_atual)}/{dim_lista_compartilhada} ===')
    for index, andar in enumerate(chamadas_por_andar):
        info = list()
        for dados_usuario in andar:
            info.append([dados_usuario['Nome'], dados_usuario['Andar Partida'], dados_usuario['Andar Chegada']])
        print(f'{index + 1}: {info}')

def visualiza_lista_compartilhada():
    
    info = list()
    for acao in lista_compartilhada:
        info.append([acao['Andar Partida'], acao['Andar Chegada']])
    
    print('=== Lista Compartilhada ===')
    print(info)

def visualiza_processo_atual():

    if len(chamado_atual) != 0:
        info = [chamado_atual[0]['Nome'], chamado_atual[0]['Andar Partida'], chamado_atual[0]['Andar Chegada']]
    else:
        info = chamado_atual

    print(f'Processo Atual do Elevador: {info}')

def visualiza_elevador():

    dados = gestao_elevador.get_dados_elevador()
    largura_fixa = 10

    try:
        dados_residente = pessoas.get_dados_residente(id_residente = chamado_atual[0]['ID'])
        
        print('=== Operação do Elevador ==')
        print(f"Status: {dados['Status']} | Andar: Atual {dados['Andar Atual']} -> Chegada {dados['Andar Chegada']}")
        for andar in range(max_andar, -1, -1):
            if dados['Andar Atual'] == andar:
                if dados_residente['Status'] == 'em espera' and dados_residente['Andar Partida'] == andar:
                    print(f"{andar}: {dados_residente['Nome'].ljust(largura_fixa)} [X]")
                elif dados_residente['Status'] == 'no elevador':
                    print(f"{andar}: {''.ljust(largura_fixa)} [{dados_residente['Nome']}]")
                else:
                    print(f"{andar}: {''.ljust(largura_fixa)} [X]")
            else:
                if dados_residente['Status'] == 'em espera' and dados_residente['Andar Partida'] == andar:
                    print(f"{andar}: {dados_residente['Nome'].ljust(largura_fixa)}")
                else:
                    print(f"{andar}:")
    except:
        pass


def interface():

    while True:
        
        titulo = " Prédio Jambalaya Ocean Drive "
        decoracao = "=" * (len(titulo) + 4)  # Ajusta a largura da decoração
    
        print(decoracao)
        print(f"|{titulo.center(len(decoracao) - 2)}|")
        print(decoracao)
        print('\n')

        visualiza_lista_por_andar()
        print('---\n')
        visualiza_lista_compartilhada()
        print('--\n')
        visualiza_processo_atual()
        print('--\n')
        visualiza_elevador()

        time.sleep(0.25)
        os.system('clear')

t1 = threading.Thread(target = solicita_elevador)
t2 = threading.Thread(target = interface)
t3 = threading.Thread(target = processa_chamado)
t4 = threading.Thread(target = move_elevador)

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()
