import csv 
import json
from datetime import datetime


class AgentLogger:
    def __init__(self, log_file, csv_file):
        self.log_file = log_file
        self.csv_file = csv_file
        self.logs = []

    def log_run(self, agent_name, task, tokens_used, success):
        entery = {"agent_name": agent_name, "task": task, "tokens_used":tokens_used, "success": success, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self.logs.append(entery)
    
    def save_to_csv(self):
        with open(self.csv_file, "w") as file:
            writer = csv.DictWriter(file, fieldnames=["agent_name", "task", "tokens_used", "success", "timestamp"])
            writer.writeheader()
            writer.writerows(self.logs)

    def save_to_json(self):
        with open(self.log_file, "w") as file:
            json.dump(self.logs, file, indent=4)
    
    def get_successful_runs(self):
        return [li for li in self.logs if li["success"]==True]
    
    def get_total_tokens(self):
        return sum(s["tokens_used"] for s in self.logs)
    
    def get_summary(self):
        print(f"Total runs: {len(self.logs)}")
        print(f"Successful: {sum(1 for c in self.logs if c['success'])}") 
        print(f"Failed: {sum(1 for c in self.logs if not c['success'])}") 
        print(f"Total tokens used: {self.get_total_tokens()}")
        print(f"Most recent: {self.logs[-1]['timestamp']}")


    

logger = AgentLogger("logs.json", "logs.csv")

logger.log_run("ResearchBot", "Find AI papers", 1200, True)
logger.log_run("WriterBot", "Write blog post", 800, True)
logger.log_run("ReviewBot", "Review content", 600, False)
logger.log_run("ResearchBot", "Find ML papers", 1100, True)
logger.log_run("WriterBot", "Write summary", 800, True)

logger.save_to_csv()
logger.save_to_json()
logger.get_summary()

successful = logger.get_successful_runs()
print(f"\nSuccessful runs: {len(successful)}")
for run in successful:
    print(f"  {run['agent_name']} — {run['task']}")

