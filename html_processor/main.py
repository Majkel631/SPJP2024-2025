import argparse
from config.loader import load_config
from pipeline.runner import run_pipeline
from utils.logger import log_info, log_error

def main():
    parser = argparse.ArgumentParser(description='HTML to PDF processor')
    parser.add_argument('config', help='Path to config JSON file')
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        run_pipeline(config)
        log_info("Application finished successfully.")
    except Exception as e:
        log_error(f"Application failed: {e}")

if __name__ == "__main__":
    main()