import logging
import os
from datetime import datetime

LOG_DIR = "storage/logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

current_date = datetime.now().strftime("%Y-%m-%d")
log_file = os.path.join(LOG_DIR, f"logs.{current_date}.log")

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
file_handler.setFormatter(formatter)

logger = logging.getLogger()

if not logger.hasHandlers():
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)