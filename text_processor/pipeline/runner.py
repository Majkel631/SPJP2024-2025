import os
from pipeline.steps.reader import read_file
from pipeline.steps.transformer import apply_transformations
from pipeline.steps.writer import write_file
from utils.logger import log_info, log_error

def run_pipeline(config):
    input_dir = config["input_dir"]
    output_dir = config["output_dir"]
    transformations = config["transformations"]
    overwrite = config.get("overwrite_output", False)

    os.makedirs(output_dir, exist_ok=True)

    files = os.listdir(input_dir)
    success_count = 0
    error_count = 0

    log_info(f"Reading files from: {input_dir}")
    for file in files:
        input_path = os.path.join(input_dir, file)
        try:
            text = read_file(input_path)
            log_info(f"Successfully read file: {file}")
        except Exception as e:
            log_error(f"Failed to read file {file}: {e}")
            error_count += 1
            continue

        try:
            log_info(f"Processing file: {file}...")
            file_transformations = transformations.get(file, [])
            transformed = apply_transformations(text, file_transformations)
            output_path = os.path.join(output_dir, file)
            write_file(output_path, transformed, overwrite)
            log_info(f"Successfully wrote processed file: {output_path}")
            success_count += 1
        except Exception as e:
            log_error(f"Failed to process file {file}: {e}")
            error_count += 1

    log_info("--------------------")
    log_info("Pipeline finished.")
    log_info(f"Successfully processed/written: {success_count} files.")
    if error_count:
        log_error(f"Encountered errors while processing: {error_count} files.")

    if config.get("generate_report_plot"):
        from .reporter import generate_summary_plot
        plot_path = os.path.join(output_dir, "processing_summary.png")
        log_info("Generating summary plot...")
        try:
            generate_summary_plot({"success": success_count, "error": error_count}, plot_path)
            log_info(f"Summary plot saved to: {plot_path}")
        except Exception as e:
            log_error(f"Failed to generate summary plot: {e}")

    log_info("--------------------")
    log_info("Application finished successfully.")
