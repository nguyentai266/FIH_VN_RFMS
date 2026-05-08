import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(logger_name="Log", log_filename="system.log"):
   
    if not os.path.exists('Log'):
        os.makedirs('Log')

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # ==========================================
    # CẤU HÌNH GHI LẠI VỊ TRÍ FILE (THE MAGIC HERE)
    # ==========================================
    # %(filename)s: Tên file (VD: db_manager.py)
    # %(lineno)d: Dòng số mấy (VD: 45)
    # %(funcName)s: Đang chạy trong hàm nào (VD: create_pool)
    # %(processName)s: Tên tiến trình (rất hữu ích khi chạy đa luồng)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] --> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

   

    # Xử lý log ra màn hình (Console)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Xử lý log ra File (Cắt file nếu quá 5MB)
    file_handler = RotatingFileHandler(
        f'Log/{log_filename}', maxBytes=5*1024*1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Tránh ghi log trùng lặp nếu gọi hàm nhiều lần
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

db_logger = setup_logger(logger_name="Database",log_filename="db_manager.log")
web_logger = setup_logger(logger_name="WebApp", log_filename="web_app.log")
worker_logger = setup_logger(logger_name="AutoWorker", log_filename="runner_worker.log")
