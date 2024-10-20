import yaml
import time

# Load the YAML config
def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

# Execute individual actions and delays
def execute_action(action, device=None, level=None):
    if action == "stop" and device == "All":
        print(f"Stopping all devices.")
    else:
        print(f"Action: {action}, Device: {device}, Level: {level}")

# Handle time delays
def handle_delay(delay):
    delay_seconds = convert_time_delay(delay)
    if delay_seconds > 0:
        print(f"Waiting for {delay}...")
        time.sleep(delay_seconds)

# Convert time delay (s/m) to seconds
def convert_time_delay(time_delay):
    if 's' in time_delay:
        return int(time_delay.replace('s', ''))
    elif 'm' in time_delay:
        return int(time_delay.replace('m', '')) * 60
    else:
        return 0

# Main function to handle the sequence of actions
def handle_sequence(config_file):
    config = load_config(config_file)
    sequence = config.get('c1', [])  # Use 'c1' as the key for sequence

    for step in sequence:
        if 'action' in step:
            action = step['action']
            device = step.get('device')
            level = step.get('level')
            execute_action(action, device, level)
        elif 'delay' in step:
            delay = step['delay']
            handle_delay(delay)

if __name__ == "__main__":
    handle_sequence('sequences/test.yaml')
