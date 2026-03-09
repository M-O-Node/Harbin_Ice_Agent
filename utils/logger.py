import logging
import os


def setup_logger(name='harbin_agent'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 避免重复绑定 Handler
    if not logger.handlers:
        # 统一输出到一个文件
        fh = logging.FileHandler('agent_system.log', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
