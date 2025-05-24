import matplotlib.pyplot as plt
from utils.logger import log_info, log_error

def generate_summary_plot(stats, output_path):
    try:
        labels = list(stats.keys())
        values = list(stats.values())
        plt.bar(labels, values, color=["green", "red"])
        plt.title("File Processing Summary")
        plt.xlabel("Status")
        plt.ylabel("Count")
        plt.savefig(output_path)
        plt.close()
        log_info(f"Summary plot saved to: {output_path}")
    except Exception as e:
        log_error(f"Error generating summary plot: {e}")
