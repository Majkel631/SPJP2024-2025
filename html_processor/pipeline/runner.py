import os
from .steps import parser, analyzer, generator
from utils.logger import log_info, log_error

import os
from .steps import parser, analyzer, generator
from utils.logger import log_info, log_error

def run_pipeline(config):
    input_dir = config['input_dir']
    output_dir = config['output_dir']
    overwrite = config['overwrite_output']
    stats = {'success': 0, 'error': 0, 'total_records': 0}

    log_info(f"Parsing HTML files from: {input_dir}")
    parsed_files = parser.parse_html_files(input_dir)

    analyzed_data = []
    for file_data in parsed_files:
        if 'error' in file_data:
            stats['error'] += 1
            log_error(f"Failed to parse file {file_data['filename']}: {file_data['error']}")
            continue

        log_info(f"Successfully parsed file: {file_data['filename']} ({len(file_data['records'])} records)")
        stats['success'] += 1
        stats['total_records'] += len(file_data['records'])

        analysis = analyzer.analyze_data(file_data, config.get('analysis_options'))
        analyzed_data.append({
            'filename': file_data['filename'],
            'data': analysis
        })

    log_info("Generating PDF reports...")
    generator.generate_pdf_reports(analyzed_data, output_dir, overwrite)

    log_info("--------------------")
    log_info("Pipeline finished.")
    log_info(f"Successfully processed: {stats['success']} files ({stats['total_records']} total records).")
    if stats['error'] > 0:
        log_error(f"Encountered errors: {stats['error']} files.")

    if config.get('generate_report_plot'):
        from .reporter import generate_summary_plot
        plot_path = os.path.join(output_dir, 'processing_summary.png')
        log_info("Generating summary plot...")
        generate_summary_plot(stats, plot_path)