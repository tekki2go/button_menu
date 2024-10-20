import yaml
import time
import pigpio

raspberry_pi_ip = "10.10.23.231"

# Connect to the Raspberry Pi remotely
pi = pigpio.pi(raspberry_pi_ip)

if not pi.connected:
    print("Failed to connect to Raspberry Pi.")
    exit()

# Load the YAML config for GPIO pin mapping
def load_gpio_config(gpio_config_file):
    with open(gpio_config_file, 'r') as file:
        return yaml.safe_load(file)

# Load the YAML config for action sequences
def load_action_config(action_config_file):
    with open(action_config_file, 'r') as file:
        return yaml.safe_load(file)

# Setup GPIO pins using pigpio for controlling GPIO pins
def setup_gpio_pins(pi, pin_mapping):
    for device, pin in pin_mapping.items():
        pi.set_mode(pin, pigpio.OUTPUT)  # Set each pin as OUTPUT
        pi.write(pin, 1) # Turn off the device by setting the GPIO pin high

# Execute individual actions and delays using pigpio for GPIO control
def execute_action(pi, pin_mapping, action, device=None, level=None):
    if action == "stop" and device == "All":
        print(f"Stopping all devices.")
        for pin in pin_mapping.values():
            pi.write(pin, 1)  # Turn off all devices
    elif action == "start":
        gpio_pin = pin_mapping.get(device.lower())
        if gpio_pin is not None:
            print(f"Starting {device} at level {level} on GPIO pin {gpio_pin}")
            pi.write(gpio_pin, 0)  # Turn on the device by setting the GPIO pin low
    elif action == "stop":
        gpio_pin = pin_mapping.get(device.lower())
        if gpio_pin is not None:
            print(f"Stopping {device} on GPIO pin {gpio_pin}")
            pi.write(gpio_pin, 1)  # Turn off the device by setting the GPIO pin high

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
def handle_sequence(action_config_file, gpio_config_file):
    global pi
    # Load the configs
    action_config = load_action_config(action_config_file)
    gpio_config = load_gpio_config(gpio_config_file)
    
    # Extract GPIO pin mappings
    pin_mapping = gpio_config['settings']['gpio']
    
    # Setup GPIO pins
    setup_gpio_pins(pi, pin_mapping)
    
    # Handle the sequence of actions
    sequence = action_config.get('c1', [])  # Use 'c1' as the key for sequence

    for step in sequence:
        if 'action' in step:
            action = step['action']
            device = step.get('device')
            level = step.get('level')
            execute_action(pi, pin_mapping, action, device, level)
        elif 'delay' in step:
            delay = step['delay']
            handle_delay(delay)

    # Cleanup GPIO (optional)
    pi.stop()

if __name__ == "__main__":
    # Ensure the script is not attempting to use GPIO on the local machine
    if pi.connected:
        handle_sequence('config/c1.yaml', 'config/settings.yaml')
    else:
        print("Script should only connect to the remote Raspberry Pi. Make sure the Raspberry Pi is accessible.")
