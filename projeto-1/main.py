
from residentes import simulacao_residentes
from elevador import simulacao_elevador
import threading
import random
import time

residentes = ['Celinha', 'Mário', 'Rita', 'Arnaldo', 'Isadora', 'Álvara', 'Bozena',
             'Tatalo', 'Copellia', 'Deise', 'Ladir']

pessoas = simulacao_residentes(nome_residentes = residentes)
gestao_elevador = simulacao_elevador(andar_inicial = 0)
print(gestao_elevador.get_dados_elevador())
gestao_elevador.set_chegada(5)
gestao_elevador.set_status(1)
print(gestao_elevador.get_dados_elevador())
gestao_elevador.movimenta_elevador()
print(gestao_elevador.get_dados_elevador())
gestao_elevador.movimenta_elevador()
print(gestao_elevador.get_dados_elevador())
gestao_elevador.movimenta_elevador()
print(gestao_elevador.get_dados_elevador())
gestao_elevador.movimenta_elevador()
print(gestao_elevador.get_dados_elevador())
gestao_elevador.movimenta_elevador()
print(gestao_elevador.get_dados_elevador())
gestao_elevador.movimenta_elevador()
print(gestao_elevador.get_dados_elevador())
max_floor = 5
calls_by_floor = [list()] * max_floor
# Garante que todos os residentes possam pedir ao mesmo tempo e um adicional de 5 visitas
shared_queue = len(residentes) + 5

