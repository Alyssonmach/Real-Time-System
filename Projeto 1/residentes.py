class simulacao_residentes():

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
    
    def __cria_dicionario_gestao(self):
        '''
        Cria um dicionário de gestão de usuários.

        Args:
            None
        
        Returns:
            controle_residentes (dict): Dicionário com o status de cada residente.
        '''

        controle_residentes = list()
        count = 0
        for residente in self.lista_nomes:
            count += 1
            controle_residentes.append({'ID': count, 'Nome': residente, 'Status': 'ocioso'})
        
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

        opcoes = ['ocioso', 'em espera', 'no elevador']

        for dados_residente in self.gestao:
            print(dados_residente['ID'])
            if dados_residente['ID'] == id_residente:
                try:
                    dados_residente['Status'] = opcoes[seleciona_status]
                    return 1 
                except:
                    return 0
                
        return 0




