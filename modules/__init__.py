from logging import basicConfig, getLogger, DEBUG, INFO, FileHandler, StreamHandler, Formatter
import sys
from .browser import run_browser
from .requests import run_requests
from .doc_gen import run_docx_generate
from .novel_translator import translate_novel

__all__ = ['run_browser', 'run_requests',
           'run_docx_generate', 'translate_novel']


def setup_logging():
    # Configura o logger do httpx para suprimir mensagens de DEBUG
    httpx_logger = getLogger("httpx")
    httpx_logger.setLevel(INFO)  # Ou qualquer outro nível desejado

    logger = getLogger(__name__)

    file_handler = FileHandler('app.log', 'w', encoding='utf-8')
    file_handler.setLevel(DEBUG)
    file_handler.setFormatter(
        Formatter('[%(levelname)s] - %(asctime)s - %(message)s'))

    stream_handler = StreamHandler()
    stream_handler.setLevel(DEBUG)

    basicConfig(level=DEBUG,
                format='[%(levelname)s] - %(asctime)s - %(message)s',
                datefmt='%H:%M:%S', encoding='utf-8',
                handlers=[file_handler, stream_handler])

    # Configura o hook de exceção para registrar exceções não capturadas.
    def log_unhandled_exception(exc_type, exc_value, exc_traceback):
        logger.critical("Ocorreu um erro inesperado", exc_info=(
            exc_type, exc_value, exc_traceback))

    # Substitui o hook de exceção padrão
    sys.excepthook = log_unhandled_exception

    return logger


logger = setup_logging()
