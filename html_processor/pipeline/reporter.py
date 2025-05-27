import matplotlib.pyplot as plt
from utils.logger import log_info, log_error

def generate_summary_plot(stats, output_path):
    try:
        labels = ['Success', 'Error', 'Records']
        values = [stats['success'], stats['error'], stats['total_records']]

        plt.bar(labels, values, color=['green', 'red', 'blue'])
        plt.title("HTML to PDF Processing Summary")
        plt.savefig(output_path)
        plt.close()
        log_info(f"Summary plot saved to: {output_path}")
    except Exception as e:
        log_error(f"Failed to generate plot: {e}")
