import csv
import datetime

class ResultsLogger:
    def __init__(self):
        self.results = []

    def log_result(self, model_name, prompt_name, result):
        entry = {
            "model": model_name,
            "prompt": prompt_name,
            "status": result.get("completion_status", "Unknown"),
            "iterations": result.get("iterations", 0),
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.results.append(entry)
        print(f"DEBUG: Logged result: {entry}")  # Add this


    def log_error(self, model_name, prompt_name, error_message):
        entry = {
            "model": model_name,
            "prompt": prompt_name,
            "status": "Error",
            "error_message": error_message,
            "iterations": 0,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.results.append(entry)

    def save_csv(self, filename=None):
        if not self.results:
            print("No results to save!")
            return

        if filename is None:
            filename = f"benchmark_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.results[0].keys())
                writer.writeheader()
                for row in self.results:
                    writer.writerow(row)
        except Exception as e:
            print(f"ERROR saving CSV: {e}")
            return

        print(f"Saved results to {filename}")

    def clear(self):
        self.results = []
