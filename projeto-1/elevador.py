
from residentes import simulacao_residentes
import threading
import random
import time

residentes = ['Celinha', 'Mário', 'Rita', 'Arnaldo', 'Isadora', 'Álvara', 'Bozena',
             'Tatalo', 'Copellia', 'Deise', 'Ladir']

pessoas = simulacao_residentes(nome_residentes = residentes)

for index, residente in enumerate(residentes):

    print('Antes:\n')
    print(pessoas.get_gestao())
    print('--\n')
    print(pessoas.inicia_chamada(max_andares = 5))
    print('\nDepois:\n')
    print(pessoas.get_gestao())

print('\nAntes:\n')
print(pessoas.get_gestao())
print('--\n')
print(pessoas.inicia_chamada(max_andares = 5))
print('Depois:\n')
print(pessoas.get_gestao())


max_floor = 5
calls_by_floor = [list()] * max_floor
# Garante que todos os residentes possam pedir ao mesmo tempo e um adicional de 5 visitas
shared_queue = len(residentes) + 5

