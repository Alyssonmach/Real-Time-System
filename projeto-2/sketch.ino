#include <Arduino_FreeRTOS.h>
#include <queue.h>
#include <semphr.h>

#define TEMPO_OPERACAO_ROBO 100
#define TEMPO_MOVIMENTO_R1_R2_R4 500
#define TEMPO_PRODUCAO_M1_M2 1500

// Semáforos para controle dos ítens na entrada e saída das máquinas
SemaphoreHandle_t xtemEntradaCelula;
SemaphoreHandle_t xtemSaidaCelula;
// Semáforo que indica se o robô está em movimento ou não
SemaphoreHandle_t xmoveR1;

SemaphoreHandle_t xtemEntradaM1;
SemaphoreHandle_t xtemSaidaM1;
SemaphoreHandle_t xmoveR2;

SemaphoreHandle_t xtemEntradaM2;
SemaphoreHandle_t xtemSaidaM2;
SemaphoreHandle_t xmoveR4;

SemaphoreHandle_t xtemEntradaM4;
SemaphoreHandle_t xtemSaidaM4;

// Filas para controle de ítens presentes nas máquinas
QueueHandle_t qFilaCelula;
QueueHandle_t qFilaM1;
QueueHandle_t qFilaM2;
QueueHandle_t qFilaM4;

// Escopo das funções de controle dos robôs
void vRoboR1(void *pvParameters);
void vRoboR2(void *pvParameters);
void vRoboR4(void *pvParameters);

// Escopo das funções de controle das máquinas
void vMaquinaCelula(void *pvParameters);
void vMaquinaM1(void *pvParameters);
void vMaquinaM2(void *pvParameters);
void vMaquinaM4(void *pvParameters);

void setup() {

  Serial.begin(9600); // Inicializa a comunicação serial com baud rate de 9600
  while (!Serial); // Aguarda a inicialização da porta serial

  // Criando os semáforos
  xtemEntradaCelula = xSemaphoreCreateBinary();
  xtemSaidaCelula = xSemaphoreCreateBinary();
  xmoveR1 = xSemaphoreCreateBinary();

  xtemEntradaM1 = xSemaphoreCreateBinary();
  xtemSaidaM1 = xSemaphoreCreateBinary();
  xmoveR2 = xSemaphoreCreateBinary();

  xtemEntradaM2 = xSemaphoreCreateBinary();
  xtemSaidaM2 = xSemaphoreCreateBinary();
  xmoveR4 = xSemaphoreCreateBinary();

  xtemEntradaM4 = xSemaphoreCreateBinary();
  xtemSaidaM4 = xSemaphoreCreateBinary();

  // Inicia com espaço disponível na entrada das máquinas
  xSemaphoreGive(xtemEntradaCelula);
  xSemaphoreGive(xtemEntradaM1);
  xSemaphoreGive(xtemEntradaM2);
  xSemaphoreGive(xtemEntradaM4);

  Serial.println("Iniciando a jornada!");

  // Criando as filas para controle de quantidade de itens nas máquinas
  qFilaCelula = xQueueCreate(1, sizeof(int));
  qFilaM1 = xQueueCreate(1, sizeof(int));
  qFilaM2 = xQueueCreate(1, sizeof(int));
  qFilaM4 = xQueueCreate(1, sizeof(int));

  // Criação das tarefas
  xTaskCreate(vMaquinaCelula, "Máquina Célula", 128, NULL, 1, NULL);
  xTaskCreate(vMaquinaM1, "Maquina M1", 128, NULL, 1, NULL);
  xTaskCreate(vRoboR1, "Robo R1", 128, NULL, 2, NULL);
  xTaskCreate(vMaquinaM2, "Maquina M2", 128, NULL, 1, NULL);
  xTaskCreate(vRoboR2, "Robo R2", 128, NULL, 2, NULL);
  xTaskCreate(vRoboR4, "Robo R4", 128, NULL, 2, NULL);
  xTaskCreate(vMaquinaM4, "Maquina M4", 128, NULL, 1, NULL);
  
  // Inicia as tarefas
  vTaskStartScheduler();
}

void loop() {}

void vMaquinaCelula(void *pvParameters) {
  (void) pvParameters;
  int item = 0;
  
  while (1) {
    if (xSemaphoreTake(xtemEntradaCelula, portMAX_DELAY) == pdTRUE) {
      Serial.println("Celula: Item na Entrada, processando...");
      //  converter milissegundos em ticks do sistema
      vTaskDelay(pdMS_TO_TICKS(TEMPO_PRODUCAO_M1_M2));
      xQueueSend(qFilaCelula, &item, portMAX_DELAY);
      Serial.println("Celula: Item pronto na saida");
      xSemaphoreGive(xtemSaidaCelula);
      xSemaphoreGive(xmoveR1);
    }
  }
}

void vRoboR1(void *pvParameters) {
  (void) pvParameters;
  int item;
  
  while (1) {
    if (xSemaphoreTake(xmoveR1, portMAX_DELAY) == pdTRUE) {
      Serial.println("R1: Movendo para Célula");
      vTaskDelay(pdMS_TO_TICKS(TEMPO_MOVIMENTO_R1_R2_R4));

      Serial.println("R1: Retirando da Célula");
      vTaskDelay(pdMS_TO_TICKS(TEMPO_OPERACAO_ROBO));

      Serial.println("R1: Movendo para M1");
      vTaskDelay(pdMS_TO_TICKS(TEMPO_MOVIMENTO_R1_R2_R4));
      if (xSemaphoreTake(xtemEntradaM1, portMAX_DELAY) == pdTRUE) {
        Serial.println("R1: Depositando em M1");
        // Bloqueia o semáforo para indicar que não há mais saída na máquina anterior
        if (xSemaphoreTake(xtemSaidaCelula, portMAX_DELAY) == pdTRUE)  {
          vTaskDelay(pdMS_TO_TICKS(TEMPO_OPERACAO_ROBO));
          xQueueReceive(qFilaCelula, &item, portMAX_DELAY);
          xQueueSend(qFilaM1, &item, portMAX_DELAY);
          // Indica que a entrada da máquina anterior está vazia
          xSemaphoreGive(xtemEntradaCelula);
        }
      }
    }
  }
}

void vMaquinaM1(void *pvParameters) {
  (void) pvParameters;
  int item = 0;
  
  while (1) {
    // Verifica se tem um item na pilha
    if (!uxQueueSpacesAvailable(qFilaM1) > 0) {
      // Verifica se o semáforo está bloqueado, indicando que não há nenhum item na saída
      if (uxSemaphoreGetCount(xtemSaidaM1) == 0) {
        Serial.println("M1: Item na Entrada, processando...");
        vTaskDelay(pdMS_TO_TICKS(TEMPO_PRODUCAO_M1_M2));

        Serial.println("M1: Item pronto na saida");
        // Indica que tem um pacote na saída
        xSemaphoreGive(xtemSaidaM1);
        // Autoriza a vinda do robô
        xSemaphoreGive(xmoveR2);

      }
    }
  }
}

void vRoboR2(void *pvParameters) {
  (void) pvParameters;
  int item;
  
  while (1) {
    if (xSemaphoreTake(xmoveR2, portMAX_DELAY) == pdTRUE) {
        Serial.println("R2: Movendo para M1");
        vTaskDelay(pdMS_TO_TICKS(TEMPO_MOVIMENTO_R1_R2_R4));

        Serial.println("R2: Retirando de M1");
        vTaskDelay(pdMS_TO_TICKS(TEMPO_OPERACAO_ROBO));

        Serial.println("R2: Movendo para M2");
        vTaskDelay(pdMS_TO_TICKS(TEMPO_MOVIMENTO_R1_R2_R4));

        if (xSemaphoreTake(xtemEntradaM2, portMAX_DELAY) == pdTRUE) {
          Serial.println("R2: Depositando em M2");
          if (xSemaphoreTake(xtemSaidaM1, portMAX_DELAY) == pdTRUE) {
            vTaskDelay(pdMS_TO_TICKS(TEMPO_OPERACAO_ROBO));
            xQueueReceive(qFilaM1, &item, portMAX_DELAY);
            xQueueSend(qFilaM2, &item, portMAX_DELAY);
            xSemaphoreGive(xtemEntradaM1);
          }
        }
  } }
}

void vMaquinaM2(void *pvParameters) {
  (void) pvParameters;
  int item = 0;
  
  while (1) {
    if (!uxQueueSpacesAvailable(qFilaM2) > 0) {
      if (uxSemaphoreGetCount(xtemSaidaM2) == 0) {
        Serial.println("M2: Item na Entrada, processando...");
        vTaskDelay(pdMS_TO_TICKS(TEMPO_PRODUCAO_M1_M2));

        Serial.println("M2: Item pronto na saida");
        xSemaphoreGive(xtemSaidaM2);
        xSemaphoreGive(xmoveR4);
      }
    }
  }
}

  

void vRoboR4(void *pvParameters) {
  (void) pvParameters;
  int item;
  
  while (1) {
    if (xSemaphoreTake(xmoveR4, portMAX_DELAY) == pdTRUE) {
      Serial.println("R4: Movendo para M2");
      vTaskDelay(pdMS_TO_TICKS(TEMPO_MOVIMENTO_R1_R2_R4));

      Serial.println("R4: Retirando de M2");
      vTaskDelay(pdMS_TO_TICKS(TEMPO_OPERACAO_ROBO));

      Serial.println("R4: Movendo para M4");
      vTaskDelay(pdMS_TO_TICKS(TEMPO_MOVIMENTO_R1_R2_R4));

      if (xSemaphoreTake(xtemEntradaM4, portMAX_DELAY) == pdTRUE) {
        Serial.println("R4: Depositando em M4");
        if (xSemaphoreTake(xtemSaidaM2, portMAX_DELAY) == pdTRUE) {
          vTaskDelay(pdMS_TO_TICKS(TEMPO_OPERACAO_ROBO));
          xQueueReceive(qFilaM2, &item, portMAX_DELAY);
          xQueueSend(qFilaM4, &item, portMAX_DELAY);
          xSemaphoreGive(xtemEntradaM2);
        }
      }
    } 
  }
}

void vMaquinaM4(void *pvParameters) {
  (void) pvParameters;
  int item = 0;
  
  while (1) {
    if (!uxQueueSpacesAvailable(qFilaM4) > 0) {
      if (uxSemaphoreGetCount(xtemSaidaM4) == 0) {
        Serial.println("M4: Item na Entrada, processando...");
        vTaskDelay(pdMS_TO_TICKS(TEMPO_PRODUCAO_M1_M2));

        Serial.println("M4: Item entregue para Transporte");
        xQueueReceive(qFilaM4, &item, portMAX_DELAY);
        xSemaphoreGive(xtemEntradaM4);
        
      }
    }
  }
}
