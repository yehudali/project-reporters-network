import logging
import sys

class AppLogger:
    @staticmethod
    def get_logger(name: str):
        logger = logging.getLogger(name)
        
        if not logger.handlers:
            logger.setLevel(logging.INFO)

            handler = logging.StreamHandler(sys.stdout)
            
        
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            
            logger.addHandler(handler)
            
        return logger