import logging

class Logger:
    """
    Classe responsável por configurar e gerenciar o registro de logs em um arquivo.

    Atributos:
        log_file (str): Nome do arquivo de log. Padrão: "erros_processamento_despesa.log".
        log_level (int): Nível mínimo de mensagens a serem registradas. Padrão: logging.ERROR.
    """

    def __init__(self, log_file="erros_processamento_despesa.log", 
                       log_level = logging.ERROR):
        """
        Inicializa uma instância da classe Logger.

        Args:
            log_file (str): Nome do arquivo de log. Padrão: "erros_processamento_despesa.log".
            log_level (int): Nível mínimo de mensagens a serem registradas. Padrão: logging.ERROR.
        """
        self.log_file = log_file
        self.log_level = log_level

        # Configuração do logging
        logging.basicConfig(
            filename = self.log_file,
            level = self.log_level,
            format = "%(asctime)s \t %(levelname)s \t %(message)s",
            datefmt = "%Y-%m-%d"
        )

    def log_error(self, message):
        """
        Registra uma mensagem de erro no arquivo de log.

        Args:
            message (str): Mensagem de erro a ser registrada.
        """
        logging.error(message)
