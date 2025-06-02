import csv
import datetime
import os

class ResultsLogger:
    def __init__(self):
        self.results = []

    def log(self, model_name, prompt_name, prompt_text, response_text, metadata=None):
        """Legacy method for backward compatibility"""
        entry = {
            "model": model_name,
            "prompt": prompt_name,
            "prompt_text": prompt_text[:100] + "..." if len(prompt_text) > 100 else prompt_text,
            "response_text": response_text[:200] + "..." if len(response_text) > 200 else response_text,
            "status": "Completed",
            "iterations": metadata.get("conversation_length", 0) if metadata else 0,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.results.append(entry)
        print(f"DEBUG: Logged result via log(): {entry}")

    def log_result(self, model_name, prompt_name, result):
        """Enhanced method for detailed results"""
        entry = {
            "model": model_name,
            "prompt": prompt_name,
            "status": result.get("completion_status", "Unknown"),
            "iterations": result.get("iterations", 0),
            "command_count": len(result.get("command_results", [])),
            "final_status": result.get("completion_status", "Unknown"),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Add command history summary if available
        if "command_results" in result:
            successful_commands = sum(1 for cmd in result["command_results"] 
                                    if cmd.get("result", {}).get("return_code") == 0)
            entry["successful_commands"] = successful_commands
        
        self.results.append(entry)
        print(f"DEBUG: Logged result via log_result(): {entry}")

    def log_error(self, model_name, prompt_name, error_message):
        """Log error results"""
        entry = {
            "model": model_name,
            "prompt": prompt_name,
            "status": "Error",
            "error_message": error_message,
            "iterations": 0,
            "command_count": 0,
            "successful_commands": 0,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.results.append(entry)
        print(f"DEBUG: Logged error: {entry}")

    def save_csv(self, filename=None):
        """Save results to CSV file"""
        print(f"DEBUG: save_csv called with {len(self.results)} results")
        
        if not self.results:
            print("WARNING: No results to save!")
            return
        
        if filename is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"benchmark_results_{timestamp}.csv"
        
        # Ensure results directory exists
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)
        filepath = os.path.join(results_dir, filename)
        
        try:
            # Get all possible fieldnames from all results
            all_fieldnames = set()
            for result in self.results:
                all_fieldnames.update(result.keys())
            
            fieldnames = sorted(list(all_fieldnames))
            
            with open(filepath, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in self.results:
                    # Ensure all fields are present in each row
                    complete_row = {field: row.get(field, '') for field in fieldnames}
                    writer.writerow(complete_row)
            
            print(f"SUCCESS: Results saved to {filepath}")
            print(f"DEBUG: Saved {len(self.results)} results to CSV")
            
        except Exception as e:
            print(f"ERROR saving CSV to {filepath}: {e}")
            # Try saving to current directory as fallback
            try:
                fallback_path = filename
                with open(fallback_path, mode='w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in self.results:
                        complete_row = {field: row.get(field, '') for field in fieldnames}
                        writer.writerow(complete_row)
                print(f"FALLBACK: Results saved to {fallback_path}")
            except Exception as e2:
                print(f"CRITICAL ERROR: Could not save CSV anywhere: {e2}")

    def clear(self):
        """Clear all results"""
        self.results = []
        print("DEBUG: Results cleared")

    def get_summary(self):
        """Get summary statistics"""
        if not self.results:
            return "No results to summarize"
        
        total = len(self.results)
        completed = sum(1 for r in self.results if r.get("status") == "Completed")
        errors = sum(1 for r in self.results if r.get("status") == "Error")
        
        return {
            "total_tests": total,
            "completed": completed,
            "errors": errors,
            "success_rate": f"{(completed/total)*100:.1f}%" if total > 0 else "0%"
        }