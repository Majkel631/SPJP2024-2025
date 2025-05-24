from datetime import datetime

def _timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def log_info(message):
    print(f"{_timestamp()} INFO: {message}")

def log_error(message):
    print(f"{_timestamp()} ERROR: {message}")
