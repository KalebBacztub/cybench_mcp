import pandas as pd
from datetime import datetime
import os
import logging

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "mcp_interactions.log")

os.makedirs(LOG_DIR, exist_ok=True)  # Ensure logs/ exists before setting up logging

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

class ResultsLogger:
    def __init__(self, output_dir="results"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.records = []

    def log(self, model_name, prompt_name, prompt_text, response_text, metadata=None):
        timestamp = datetime.utcnow().isoformat()
        record = {
            "timestamp": timestamp,
            "model": model_name,
            "prompt_name": prompt_name,
            "prompt_text": prompt_text,
            "response_text": response_text
        }
        if metadata:
            record.update(metadata)
        self.records.append(record)
        logging.info(f"Model={model_name} Prompt={prompt_name} Metadata={metadata}")

    def save_csv(self, filename=None):
        filename = filename or f"benchmark_results_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        df = pd.DataFrame(self.records)
        df.to_csv(os.path.join(self.output_dir, filename), index=False)
        print(f"Saved results to {filename}")
