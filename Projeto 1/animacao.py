import time
import os

def desenhar_elevador(total_andares, andar_atual):
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela no Windows/Linux

    for andar in range(total_andares, -1, -1):  # Começa do topo e desce até o térreo (0)
        if andar == andar_atual:
            print(f"{andar} | 📦  ")  # Elevador presente neste andar
        else:
            print(f"{andar} | ⬜  ")  # Andar vazio

    print("\nDigite 'U' para subir, 'D' para descer, ou 'S' para sair.")

# Exemplo de uso
total_andares = 5  # Total de andares (incluindo o térreo)
andar_atual = 0  # Começa no térreo

while True:
    desenhar_elevador(total_andares, andar_atual)
    comando = input("Comando: ").strip().upper()

    if comando == 'U' and andar_atual < total_andares:
        andar_atual += 1
    elif comando == 'D' and andar_atual > 0:
        andar_atual -= 1
    elif comando == 'S':
        print("Saindo...")
        break
    else:
        print("Comando inválido!")
    
    time.sleep(0.5)  # Pequena pausa para melhor visualização
