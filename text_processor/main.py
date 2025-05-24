import argparse
import sys
from config.loader import load_config
from pipeline.runner import run_pipeline
from utils.logger import log_error

def main():
    parser = argparse.ArgumentParser(description="Text Processor Pipeline")
    parser.add_argument("config_path", type=str, help="Path to config JSON file")
    args = parser.parse_args()

    try:
        config = load_config(args.config_path)
        run_pipeline(config)
    except Exception as e:
        log_error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
