import logging
import os
import time


def write_log(msg, type_msg):
    log_dir = os.path.join('Путь к рабочему каталогу', 'logs')
    print(log_dir)
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        filename=f'{log_dir}/{time.strftime("%d%m%Y")}.log',
        format="%(asctime)s %(module)s %(levelname)s:%(message)s",
        datefmt='%H:%M:%S',
    )
    match type_msg:
        case 'info':
            logging.info(msg)
        case 'error':
            logging.error(msg)
