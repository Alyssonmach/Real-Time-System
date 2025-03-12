import random

class simulacao_residentes():
    '''
    Simula o comportamento dos residentes.
    '''

    def __init__(self, nome_residentes: list) -> None:
        '''
        Construtor da classe.

        Args:
            nome_residentes (list): Lista com o nome dos residentes.
        
        Returns:
            None
        '''

        self.lista_nomes = nome_residentes 
        self.gestao = self.__cria_dicionario_gestao()   
        self.status_residentes = ['ocioso', 'em espera', 'no elevador']
    
    def __cria_dicionario_gestao(self):
        '''
        Cria um dicionário de gestão de usuários.

        Args:
            None
        
        Returns:
            controle_residentes (dict): Dicionário com o status de cada residente.
            `ID -> ID único de cada residente`
            `Nome -> Nome do residente`
            `Status -> Situação de cada residente com referência ao elevador`
            `Andar Partida -> Andar que o residente está atualmente`
            `Andar Chegada -> Andar que o residente quer chegar`
        '''

        controle_residentes = list()
        count = 0
        for residente in self.lista_nomes:
            count += 1
            controle_residentes.append({'ID': count, 'Nome': residente, 'Status': 'ocioso',
                                        'Andar Partida': 0, 'Andar Chegada': 0})
        
        return controle_residentes
    
    def get_gestao(self):
        '''
        Retorna o dicionário com o status de cada residente.

        Args:
            None
        
        Returns:
            gestao (dict) -> Dicionário com o status atual de cada residente.
        '''

        return self.gestao
    
    def set_status(self, id_residente, seleciona_status = 0):
        '''
        Muda o status dos residentes.

        Args:
            id_residente (str): ID do residente.
            seleciona_status (int): Status do residente.
                                    `0 -> Ocioso` 
                                    `1 -> em espera` 
                                    `2 -> no elevador`
        
        Returns:
            status_operacao (bool) -> Indica se a operação foi concluida com sucesso 
            ou falhou.
        '''

        for dados_residente in self.gestao:
            if dados_residente['ID'] == id_residente:
                try:
                    dados_residente['Status'] = self.status_residentes[seleciona_status]
                    return 1 
                except:
                    return 0
                
        return 0
    
    def set_andares(self, id_residente, andar_inicial, andar_final):
        '''
        Define os andares objetivados pelo residente com relação ao elevador.

        Args:
            id_residente (str): ID do residente.
            andar_inicial (int) -> Andar na qual o residente está.
            andar_final (int) -> Andar na qual o residente quer chegar.
        
        Returns:
            None
        '''

        for dados_residente in self.gestao:
            if dados_residente['ID'] == id_residente:
                try:
                    dados_residente['Andar Partida'] = andar_inicial
                    dados_residente['Andar Chegada'] = andar_final
                    return 1
                except:
                    return 0
            
        return 0
                
    def get_por_status(self, seleciona_status):
        '''
        Retorna uma lista de residentes com determinado status em referência ao elevador.

        Args:
            seleciona_status (int): Status do residente.
                                    `0 -> Ocioso` 
                                    `1 -> em espera` 
                                    `2 -> no elevador`
        
        Returns:
            ociosos (list) -> Lista de residente que pertencem ao mesmo status.
        '''

        residentes_por_status = list()
        for dados_residente in self.gestao:
            try:
                if dados_residente['Status'] == self.status_residentes[seleciona_status]:
                    residentes_por_status.append([dados_residente['ID'], dados_residente['Nome']])
            except:
                return 0
            
        return residentes_por_status
    
    def get_dados_residente(self, id_residente):
        '''
        Retorna os dados do residente por ID.

        Args:
            id_residente (int) -> ID do residente.
        
        Returns:
            dados_residente (dict) -> Dicionário contendo as informações do residente.
        '''

        for dados_residente in self.gestao:
            try:
                if dados_residente['ID'] == id_residente:
                    return dados_residente
            except:
                return 0
        
        return 0
    
    def inicia_chamada(self, max_andares):
        '''
        Cria uma chamada de um residente ocioso para o elevador.

        Args:
            max_andares (int) -> número máximo de andares do prédio.
        
        Returns:
            status (bool) -> Indica se o chamada foi realizado ou não feito caso todos os 
            residentes estejam ocupados.
            dados_usuario (dict) -> Dados do usuário que realizou a chamada
        '''

        ociosos = self.get_por_status(seleciona_status = 0)
        if ociosos == list():
            return 0, dict()
        
        andares = list(range(1, max_andares + 1)) 
        residente_ativo = random.choice(ociosos)
        chamado = random.sample(andares, 2)

        self.set_status(id_residente = residente_ativo[0], seleciona_status = 1)
        self.set_andares(id_residente = residente_ativo[0], 
                         andar_inicial = chamado[0], 
                         andar_final =chamado[1])
        
        return 1, self.get_dados_residente(id_residente = residente_ativo[0])










