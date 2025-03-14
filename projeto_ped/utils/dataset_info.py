class DatasetInfo:
    '''
    Classe para armazenar informações sobre o processamento do dataset.
    Informações contidas:
    - Linhas processadas
    - Linhas carregadas
    - Linhas descartadas        
    '''
    _instance = None  # Atributo estático para armazenar a única instância

    def __new__(cls, *args, **kwargs):
        """
        Método especial para controlar a criação de instâncias.
        Garante que apenas uma instância da classe seja criada.
        """
        if cls._instance is None:
            cls._instance = super(DatasetInfo, cls).__new__(cls)
            cls._instance._initialized = False  # Flag para evitar re-inicialização
        return cls._instance

    def __init__(self):
        """
        Inicializa a instância única.
        """
        if not self._initialized:
            self._initialized = True  # Marca como inicializado
            self.__processed = 0  # Linhas que estão em processamento
            self.__loaded = 0  # Linhas que não possuem erro e foram adicionadas às estruturas de dados
            self.__disregard = 0  # Linhas que apresentaram algum problema e foram descartadas (cabeçalho também conta)
            
    # Métodos para processar, carregar ou descartar linhas
    def update_processed(self):
        """
        Incrementa o contador de linhas processadas.

        Este método deve ser chamado assim que uma linha do dataset é processada,
        independentemente de ter sido carregada com sucesso ou descartada.
        """
        self.__processed += 1

    def update_loaded(self):
        """
        Incrementa o contador de linhas carregadas com sucesso.

        Este método deve ser chamado quando uma linha é processada sem erros
        e adicionada às estruturas de dados.
        """
        self.__loaded += 1

    def update_disregard(self):
        """
        Incrementa o contador de linhas descartadas.

        Este método deve ser chamado quando uma linha é descartada devido a erros
        ou por ser o cabeçalho do dataset.
        """
        self.__disregard += 1
    
    # Métodos para retornar valores e exibir o progresso de leitura do .csv

    @property
    def processed(self):
        """
        Retorna o número total de linhas processadas.

        Returns:
            int: Número de linhas processadas.
        """
        return self.__processed
    
    @property
    def loaded(self):
        """
        Retorna o número total de linhas carregadas
        """
        return self.__loaded
    
    @property
    def disregard(self):
        """
        Retorna o número total de linhas descartadas
        """
        return self.__disregard
    

    def show_progress(self):
        """
        Exibe o progresso do processamento a cada 1000 linhas processadas.

        Este método verifica se o número de linhas processadas é um múltiplo de 1000
        e, se for, exibe uma mensagem de progresso no console.
        """
        if self.__processed % 1000 == 0:
            print('Progresso:', self.__processed)
