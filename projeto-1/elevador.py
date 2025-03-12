class simulacao_elevador():
    '''
    Simula o comportamento do elevador.
    '''

    def __init__(self, andar_inicial):
        '''
        Construtor da classe.

        Args:
            andar_inicial (int) -> Andar na qual o elevador inicia.
        
        Returns:
            None
        '''
        
        self.status_elevador = ['parado', 'em movimento']
        self.gestao = self.__cria_dicionario_elevador(andar_inicial = andar_inicial)

    def __cria_dicionario_elevador(self, andar_inicial):
        '''
        Cria um dicionário com as informações do elevador.

        Args:
            andar_inicial (int) -> Andar na qual o elevador inicia.
        
        Returns:
            gestao_elevador (dict) -> Dicionário com as informações do elevador.
        '''

        gestao_elevador = {'Status': self.status_elevador[0], 'Andar Atual': andar_inicial, 'Andar Chegada': 0}

        return gestao_elevador
    
    def get_dados_elevador(self):
        '''
        Obtém um dicionário com os dados do elevador.

        Args:
            None

        Returns:
            gestao_elevador (dict) -> Dicionário com as informações do elevador.
        '''

        return self.gestao
    
    def set_chegada(self, andar_chegada):
        '''
        Define um novo ponto de chegada para o elevador.

        Args:
            andar_chegada (int) -> Define o local de destino para o usuário.
        '''

        self.gestao['Andar Chegada'] = andar_chegada
    
    def set_status(self, id_status):
        '''
        Define um novo status para o elevaor.

        Args:
            id_status (int): Número do status a ser adicionado: 
                             `0 -> parado` e `1 -> em movimento`
        
        Returns:
            status (bool): Indica que a operação concluiu com sucesso `True` ou
            houve algum problema `False`
        '''
        
        try:
            self.gestao['Status'] = self.status_elevador[id_status]
        except:
            return 0
        
        return 1
    
    def movimenta_elevador(self):
        '''
        Movimenta o andar atual do elevador para um andar alvo.

        Args:
            None
        
        Returns:
            status (bool): Indica que a operação concluiu com sucesso (`True`) ou
            houve algum problema / elevador parado ()`False`).
        '''

        if self.gestao['Status'] == 'em movimento':
            andar_atual = self.gestao['Andar Atual']
            andar_chegada = self.gestao['Andar Chegada']

            if andar_atual == andar_chegada:
                self.gestao['Status'] = 'parado'
                return 0
            elif andar_atual > andar_chegada:
                self.gestao['Andar Atual'] -= 1
            elif andar_atual < andar_chegada:
                self.gestao['Andar Atual'] += 1
            
            return 1
        
        else:
            return 0


