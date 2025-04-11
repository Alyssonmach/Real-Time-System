# Simulação de Célula de Manufatura com FreeRTOS

## Descrição do Projeto
Este projeto implementa a simulação de uma célula de manufatura utilizando FreeRTOS. O sistema é composto por uma célula de entrada, máquinas de processamento e robôs que transportam os itens entre os diferentes pontos do processo de fabricação.

* [Link para simulação com o arduino mega no Wokwi](https://wokwi.com/projects/427822108094558209).

## Estrutura do Sistema
O sistema é composto pelos seguintes elementos:
- **Célula de Entrada**: Responsável por receber os pacotes e disponibilizá-los para processamento.
- **Máquinas de Processamento**:
  - **M1**: Primeira etapa do processamento.
  - **M2**: Segunda etapa do processamento.
  - **M4**: Etapa final do processamento.
- **Robôs**:
  - **R1**: Transporta pacotes da Célula de Entrada para a M1.
  - **R2**: Transporta pacotes da M1 para a M2.
  - **R4**: Transporta pacotes da M2 para a M4.

> **Nota**: A M3 e o R3 ainda não foram implementados. Eles seriam responsáveis por processar itens em paralelo com a M2 e transportar da M1 para M3.

## Funcionamento
1. A **Célula de Entrada** recebe um pacote sempre que sua fila estiver vazia.
2. O **R1** transporta o pacote para a **M1**.
3. A **M1** processa o pacote e disponibiliza para a saída.
4. O **R2** transporta o pacote para a **M2**.
5. A **M2** processa o pacote e disponibiliza para a saída.
6. O **R4** transporta o pacote para a **M4**.
7. A **M4** finaliza o processamento e libera o pacote para transporte final.

Cada robô e máquina possui um tempo de operação definido conforme as regras do projeto.

## Tecnologias Utilizadas
- **Arduino Mega (simulação no Wokwi)**
- **FreeRTOS** para gerenciamento de tarefas
- **Semáforos** para controle de acesso às máquinas
- **Filas** para gestão de pacotes entre os processos

## Como Rodar o Projeto
1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   ```
2. Abra o projeto no Arduino IDE ou no Wokwi.
3. Compile e carregue o código.
4. Observe o funcionamento do sistema através do Serial Monitor.

## Melhorias Futuras
- Implementação da **M3** e do **R3** para permitir um fluxo paralelo de processamento.
- Testes para otimizar o tempo de deslocamento dos robôs e reduzir paradas indesejadas.

## Autor(es)
Projeto desenvolvido para a disciplina **STR 2024.2 - Sistemas de Automação para Monitoramento Inteligente**.
Professor: `KYLLER COSTA GORGONIO`



