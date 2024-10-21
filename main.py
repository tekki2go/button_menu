# main.py

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
import threading
import yaml
import time
import pigpio
import sys

# Optional: Set window size (useful during development)
# Window.size = (400, 300)

class TaskExecutor:
    """
    TaskExecutor handles loading task configurations from YAML files and executing them
    using the pigpio library to control GPIO pins remotely via the pigpiod daemon.
    """
    LEVELS = {
        'min': 85,    # Approx. 33% Duty Cycle (255 * 0.33 ≈ 85)
        'med': 170,   # Approx. 66% Duty Cycle (255 * 0.66 ≈ 170)
        'max': 255    # 100% Duty Cycle
    }

    def __init__(self, settings_path='config/settings.yaml', pigpio_host='10.10.23.231'):
        """
        Initializes the TaskExecutor by loading GPIO settings and connecting to the pigpiod daemon.

        :param settings_path: Path to the settings YAML file.
        :param pigpio_host: IP address of the remote pigpiod daemon.
        """
        self.pigpio_host = pigpio_host
        # Load settings from settings.yaml
        try:
            with open(settings_path, 'r') as f:
                config = yaml.safe_load(f)
                self.gpio_settings = config.get('settings', {}).get('gpio', {})
        except FileNotFoundError:
            print(f"Settings file {settings_path} not found.")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML settings: {e}")
            sys.exit(1)

        # Initialize pigpio
        self.pi = pigpio.pi(self.pigpio_host)
        if not self.pi.connected:
            print(f"Unable to connect to pigpiod daemon at {self.pigpio_host}. Ensure it's running.")
            sys.exit(1)

        self.pwm_channels = {}
        self._initialize_gpio()

    def _initialize_gpio(self):
        """
        Sets up GPIO pins as outputs and initializes PWM channels.
        """
        for device, pin in self.gpio_settings.items():
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.set_PWM_range(pin, 255)  # Set PWM range to 0-255
            self.pi.set_PWM_dutycycle(pin, 0)  # Start with 0 (OFF)
            self.pwm_channels[device.lower()] = pin  # Store device names in lowercase for uniformity
            print(f"Initialized GPIO for {device} on pin {pin}")

    def execute_from_file(self, filepath):
        """
        Loads and executes a task from a YAML file.

        :param filepath: Path to the task YAML file.
        """
        try:
            with open(filepath, 'r') as file:
                task_data = yaml.safe_load(file)
                self.execute_task(task_data)
        except FileNotFoundError:
            print(f"Task file {filepath} not found.")
            raise
        except yaml.YAMLError as e:
            print(f"Error parsing YAML task file: {e}")
            raise

    def execute_task(self, task_data):
        """
        Executes a sequence of actions and delays defined in the task data.

        :param task_data: Dictionary containing task actions.
        """
        actions = task_data.get('actions', [])
        for idx, action in enumerate(actions, start=1):
            action_type = action.get('type')
            print(f"\nStep {idx}: {action_type}")
            if action_type == 'action':
                self._handle_action(action)
            elif action_type == 'delay':
                self._handle_delay(action)
            else:
                print(f"Unknown action type: {action_type}")

    def _handle_action(self, action):
        """
        Handles 'action' type steps, such as starting or stopping devices.

        :param action: Dictionary containing action details.
        """
        action_type = action.get('action_type')
        device = action.get('device').lower()  # Convert device name to lowercase for uniformity
        level = action.get('level', 'max')  # Default to 'max' if not specified

        if device == 'all':
            if action_type == 'stop':
                for dev, pin in self.pwm_channels.items():
                    self.pi.set_PWM_dutycycle(pin, 0)
                    print(f"Stopped {dev}")
            elif action_type == 'start':
                for dev, pin in self.pwm_channels.items():
                    duty_cycle = self.LEVELS.get(level, 255)
                    self.pi.set_PWM_dutycycle(pin, duty_cycle)
                    print(f"Started {dev} at {level} level ({duty_cycle}/255 duty cycle)")
            else:
                print(f"Unsupported action_type '{action_type}' for device 'All'")
            return

        if device not in self.pwm_channels:
            print(f"Unknown device: {device}")
            return

        pin = self.pwm_channels[device]

        if action_type == 'start':
            duty_cycle = self.LEVELS.get(level, 255)
            self.pi.set_PWM_dutycycle(pin, duty_cycle)
            print(f"Started {device} at {level} level ({duty_cycle}/255 duty cycle)")
        elif action_type == 'stop':
            self.pi.set_PWM_dutycycle(pin, 0)
            print(f"Stopped {device}")
        else:
            print(f"Unknown action_type: {action_type}")

    def _handle_delay(self, action):
        """
        Handles 'delay' type steps, pausing execution for a specified duration.

        :param action: Dictionary containing delay details.
        """
        amount = action.get('amount', 1)
        unit = action.get('unit', 'sec')
        if unit.startswith('sec'):
            delay_time = amount
        elif unit.startswith('min'):
            delay_time = amount * 60
        elif unit.startswith('hour'):
            delay_time = amount * 3600
        else:
            print(f"Unknown delay unit: {unit}, defaulting to seconds")
            delay_time = amount
        print(f"Delaying for {delay_time} seconds")
        time.sleep(delay_time)

    def cleanup(self):
        """
        Cleans up GPIO resources by stopping all PWM channels and disconnecting from pigpiod.
        """
        print("\nCleaning up pigpio resources.")
        for device, pin in self.pwm_channels.items():
            self.pi.set_PWM_dutycycle(pin, 0)
            print(f"Stopped PWM for {device}")
        self.pi.stop()


class MainApp(App):
    """
    MainApp is the Kivy-based GUI application that allows users to execute predefined tasks
    by clicking buttons corresponding to different configuration files.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize TaskExecutor with the remote pigpio host
        self.executor = TaskExecutor(pigpio_host='10.10.23.231')

    def build(self):
        """
        Builds the Kivy GUI layout with three buttons: C1, C2, and C3.
        Each button corresponds to a different task configuration file.
        """
        layout = GridLayout(cols=1, spacing=10, padding=10)

        button1 = Button(text='C1', size_hint=(1, 0.3))
        button2 = Button(text='C2', size_hint=(1, 0.3))
        button3 = Button(text='C3', size_hint=(1, 0.3))

        button1.bind(on_press=lambda x: self.execute_task('c1.yaml'))
        button2.bind(on_press=lambda x: self.execute_task('c2.yaml'))
        button3.bind(on_press=lambda x: self.execute_task('c3.yaml'))

        layout.add_widget(button1)
        layout.add_widget(button2)
        layout.add_widget(button3)

        return layout

    def execute_task(self, config_file):
        """
        Initiates the execution of a task in a separate thread to keep the GUI responsive.

        :param config_file: Name of the YAML configuration file to execute.
        """
        # Start task execution in a separate thread
        thread = threading.Thread(target=self._run_task, args=(config_file,))
        thread.start()

    def _run_task(self, config_file):
        """
        Executes the task and schedules a popup to inform the user of the result.

        :param config_file: Name of the YAML configuration file to execute.
        """
        try:
            self.executor.execute_from_file(f'config/{config_file}')
            # Schedule the popup on the main thread
            Clock.schedule_once(lambda dt: self.show_popup(f'Task from {config_file} executed successfully!'))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_popup(f'Error executing {config_file}: {str(e)}'))

    def show_popup(self, message):
        """
        Displays a popup with the given message.

        :param message: Message to display in the popup.
        """
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        label = Label(text=message, size_hint=(1, 0.8))
        close_button = Button(text="Close", size_hint=(1, 0.2))

        popup = Popup(title='Task Execution', content=content, size_hint=(0.8, 0.4))
        content.add_widget(label)
        content.add_widget(close_button)

        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def on_stop(self):
        """
        Ensures that GPIO resources are cleaned up when the application is closed.
        """
        self.executor.cleanup()


if __name__ == '__main__':
    MainApp().run()
