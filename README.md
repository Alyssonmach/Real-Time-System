# Sistemas em Tempo Real — UFCG

Repositório de atividades e projetos da disciplina de Sistemas em Tempo Real. Ele contém uma simulação concorrente de elevador, uma célula de manufatura com FreeRTOS e exemplos de processos, threads e semáforos.

## Conteúdo

```text
atividades/
├── fork-e-spawn/              # Criação e gerenciamento de processos em C
└── threads-e-semaforos/       # Exemplos de produtor e consumidor em Python
projeto-1/                     # Simulação de controle de elevador em Python
projeto-2/                     # Célula de manufatura com Arduino e FreeRTOS
assets/                        # Imagens usadas neste documento
```

## Projeto 1 — Sistema simplificado de controle de elevador

[Vídeo de apresentação](https://www.youtube.com/watch?v=tGET-bNy-5c)

O programa simula solicitações de residentes em um prédio de cinco andares. Threads geram e processam chamadas, movimentam o elevador e atualizam uma interface no terminal. Semáforos controlam a capacidade da fila de chamadas e o acesso ao elevador.

Os módulos principais são:

- [`projeto-1/elevador.py`](projeto-1/elevador.py): estado, destino e movimento do elevador.
- [`projeto-1/residentes.py`](projeto-1/residentes.py): estados dos residentes e geração de chamadas.
- [`projeto-1/main.py`](projeto-1/main.py): threads, sincronização e interface.

![Diagrama esquemático do sistema](assets/diagrama.png)

*Diagrama esquemático da aplicação.*

### Executar

Requer Python 3. Os módulos utilizados pertencem à biblioteca padrão.

```bash
cd projeto-1
python3 main.py
```

A interface mostra as chamadas por andar, a fila compartilhada, a chamada em atendimento e a posição do elevador. A execução é contínua; encerre com `Ctrl+C`.

![Interface do sistema no terminal](assets/interface.png)

*Visualização da interface no terminal.*

## Projeto 2 — Simulação de célula de manufatura com FreeRTOS

[Abrir simulação no Wokwi](https://wokwi.com/projects/427822108094558209) · [Vídeo de apresentação](https://www.youtube.com/watch?v=VCWOUnrepoM)

A simulação usa tarefas, filas e semáforos para coordenar o percurso de itens entre a célula de entrada, máquinas e robôs. O fluxo implementado é:

1. A célula de entrada produz um item.
2. R1 transporta o item da célula para M1.
3. M1 processa o item e R2 o leva até M2.
4. M2 processa o item e R4 o leva até M4.
5. M4 conclui o processamento e libera o item.

M3 e R3 não estão implementados. O sketch executável está em [`projeto-2/sketch.ino`](projeto-2/sketch.ino); [`projeto-2/diagram.json`](projeto-2/diagram.json) e [`projeto-2/libraries.txt`](projeto-2/libraries.txt) complementam o projeto para uso no Wokwi.

### Executar

Abra `projeto-2` no Arduino IDE ou no Wokwi, compile para Arduino Mega e carregue a simulação. Acompanhe as etapas pelo Serial Monitor.

Tecnologias usadas: Arduino Mega, FreeRTOS, semáforos e filas. O projeto foi desenvolvido para a disciplina STR 2024.2 — Sistemas de Automação para Monitoramento Inteligente (professor Kyller Costa Gorgônio).

## Atividades

### `atividades/fork-e-spawn`

Exemplo em C que demonstra criação de processos com `fork()` e `posix_spawn()`. Para compilar em sistemas POSIX com GCC, entre na pasta e execute `sh compile_program.sh`; depois, execute `./process_management`.

### `atividades/threads-e-semaforos`

Três exemplos de produtor e consumidor em Python: sincronização manual com semáforos (`exemplo1.py`), fila thread-safe (`exemplo2.py`) e encerramento após um limite de tempo (`exemplo3.py`). Execute cada exemplo com `python3 exemplo1.py`, `python3 exemplo2.py` ou `python3 exemplo3.py`, a partir da pasta correspondente. Os exemplos rodam continuamente, exceto o terceiro, que encerra após dez segundos.
