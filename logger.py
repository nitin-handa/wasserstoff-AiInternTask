# src/logger.py
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

def setup_logger():
    logger = logging.getLogger('PDFPipelineLogger')
    logger.setLevel(logging.DEBUG)
    
    handler = ConcurrentRotatingFileHandler("pipeline.log", maxBytes=5*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

logger = setup_logger()
