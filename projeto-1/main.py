
from residentes import simulacao_residentes
from elevador import simulacao_elevador
import threading
import random
import time
import os

# Definição do nome dos residentes do prédio
residentes = ['Celinha', 'Mário', 'Rita', 'Arnaldo', 'Isadora', 'Álvara', 'Bozena',
             'Tatalo', 'Copellia', 'Deise', 'Ladir']

# Definindo os parâmetros configuráveis
andar_inicial = 0
max_andar = 5
dim_lista_compartilhada = max_andar * 2

# Definindo as listas de recursos da aplicação
chamadas_por_andar = [list()] * max_andar
lista_compartilhada = list()
chamado_atual = list()

# Objetos instanciados para a classe de simulação dos residentes e do elevador
pessoas = simulacao_residentes(nome_residentes = residentes)
gestao_elevador = simulacao_elevador(andar_inicial = andar_inicial)

# Definindo os semáforos para controle das threads
capacidade_maxima_chamados = threading.Semaphore(dim_lista_compartilhada)
elevador_operante = threading.Semaphore(1)

def solicita_elevador():
    '''
    Realiza chamadas aleatórias de residentes para uso do elevador.

    Args:
        None
    
    Returns:
        None
    '''

    while True:

        capacidade_maxima_chamados.acquire() # Consome um espaço da lista compartilhada
        status, dados_usuario = pessoas.inicia_chamada(max_andares = max_andar)

        if status:
            lista_compartilhada.append(dados_usuario)

        time.sleep(random.uniform(4, 7))

def processa_chamado():
    '''
    Caso tenha chamados ativos, processa um por vez para controle do elevador.

    Args:
        None
    
    Returns:
        None
    '''

    while True:

        if len(lista_compartilhada) != 0:

            elevador_operante.acquire() # Garante uma execução por vez
            chamado_atual.append(lista_compartilhada.pop(0))

        time.sleep(1)


def move_elevador():
    '''
    Realiza o movimento do elevador a partir de comandos de controle.

    Args:
        None
    
    Returns:
        None
    '''

    status_elevador_partida = True
    status_elevador_chegada = not status_elevador_partida
    primeira_interacao = 0
    
    time.sleep(3) # Garante um tempo de ociosidade inicial

    while True:
        
        if len(chamado_atual) != 0:
            
            # Leva o elevador até o andar que o residente fez a solicitação
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
            
            # Entrega o residente no andar de chegada
            while status_elevador_chegada:
                if primeira_interacao == 0:
                    gestao_elevador.set_status(1)
                    gestao_elevador.set_chegada(chamado_atual[0]['Andar Chegada']) 
                    # Atualiza o status do residente para indicar que ele entrou no elevador
                    pessoas.set_status(id_residente = chamado_atual[0]['ID'], seleciona_status = 2)

                time.sleep(0.5)
                status_elevador_chegada =  gestao_elevador.movimenta_elevador()
                time.sleep(1)
                primeira_interacao += 1

                if status_elevador_chegada == False:
                    status_elevador_partida = True
                    primeira_interacao = 0

                    # Torna o residente ocioso a partir do momento que ele foi entrege no andar de chegada
                    pessoas.set_status(id_residente = chamado_atual[0]['ID'], seleciona_status = 0)
                    pessoas.set_andares(id_residente = chamado_atual[0]['ID'], andar_inicial = 0, andar_final = 0)

                    # Libera recursos para iniciar uma nova operação de controle do elevador a partir de um chamado
                    chamado_atual.pop(0)
                    elevador_operante.release()
                    capacidade_maxima_chamados.release()
        
        time.sleep(1)
            
            
def visualiza_lista_por_andar():
    '''
    Função para apenas plotar informação das solicitações categorizadas por andar.

    Args:
        None
    
    Returns:
        None
    '''

    for andar in range(1, max_andar + 1):
        chamados = pessoas.get_chamados_por_andar(num_andar = andar)
        chamadas_por_andar[andar - 1] = chamados

    print(f'=== Chamadas por Andar {len(lista_compartilhada) + len(chamado_atual)}/{dim_lista_compartilhada} ===')
    for index, andar in enumerate(chamadas_por_andar):
        info = list()
        for dados_usuario in andar:
            texto = f"({dados_usuario['Nome']}: I:{dados_usuario['Andar Partida']}/F:{dados_usuario['Andar Chegada']})"
            info.append(texto)
        print(f'{index + 1}: {info}')

def visualiza_lista_compartilhada():
    '''
    Função para apenas plotar as informações da lista compartilhada para controle do elevador.
    
    Args:
        None
    
    Returns:
        None
    '''
    
    info = list()
    for acao in lista_compartilhada:
        texto = f"(I:{acao['Andar Partida']}/F:{acao['Andar Chegada']})"
        info.append(texto)
    
    print('=== Lista Compartilhada ===')
    print(info)

def visualiza_processo_atual():
    '''
    Função para apenas plotar o processo atual de controle do elevador.

    Args:   
        None
    
    Returns:
        None
    '''

    if len(chamado_atual) != 0:
        info = f"({chamado_atual[0]['Nome']}: I:{chamado_atual[0]['Andar Partida']}/F:{chamado_atual[0]['Andar Chegada']})"
    else:
        info = chamado_atual

    print(f'Processo Atual do Elevador: {info}')

def visualiza_elevador():
    '''
    Função para apenas plotar uma interface simples que ilustra a localização do elevador e o posicionamento do residente.

    Args:
        None
    
    Returns:
        None
    '''

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
    '''
    Função para plotar na tela a interface da aplicação.

    Args:
        None
    
    Returns:
        None
    '''

    while True:
        
        titulo = " Prédio Jambalaya Ocean Drive "
        decoracao = "=" * (len(titulo) + 4)  # Ajusta a largura fixa da string de nome
    
        print(decoracao)
        print(f"|{titulo.center(len(decoracao) - 2)}|")
        print(decoracao)
        print('\nLegendas:\n\tI: Andar de Início\n\tF: Andar de Chegada\n')

        visualiza_lista_por_andar()
        print('---\n')
        visualiza_lista_compartilhada()
        print('--\n')
        visualiza_processo_atual()
        print('--\n')
        visualiza_elevador()

        time.sleep(0.25)
        os.system('clear')


# Definição das threads para executar diferentes funções do sistema do elevador
t1 = threading.Thread(target = solicita_elevador) # Receber solicitações do elevador
t2 = threading.Thread(target = interface) # Interface da aplicação
t3 = threading.Thread(target = processa_chamado) # Processa os pedidos e gerencia as chamadas do elevador
t4 = threading.Thread(target = move_elevador) # Controla o movimento do elevador

# Inicia todas as threads
t1.start()
t2.start()
t3.start()
t4.start()

# Aguarda a finalização de todas as threads antes de continuar a execução do programa
# (OBS: não foi implementado um sistema de controle de parada das threads)
t1.join()
t2.join()
t3.join()
t4.join()