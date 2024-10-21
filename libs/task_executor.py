import yaml

class TaskExecutor:
    def __init__(self):
        # You can load settings from settings.yaml here if needed
        with open('config/settings.yaml', 'r') as f:
            self.settings = yaml.safe_load(f)

    def execute_from_file(self, filepath):
        with open(filepath, 'r') as file:
            task_data = yaml.safe_load(file)
            self.execute_task(task_data)

    def execute_task(self, task_data):
        # Here, implement the logic that executes the steps defined in the YAML files
        for step in task_data.get('steps', []):
            print(f"Executing step: {step}")
            