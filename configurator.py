from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView  # Added import
from kivy.core.window import Window
import yaml
import os

class ConfigBuilderApp(App):
    def build(self):
        Window.size = (1200, 900)  # Set fixed size
        Window.allow_resize = False  # Disallow resizing
        self.root = BoxLayout(orientation='vertical')

        # Brick container inside ScrollView
        self.brick_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.brick_container.bind(minimum_height=self.brick_container.setter('height'))

        # ScrollView to handle bricks
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.brick_container)
        self.root.add_widget(scroll)

        # Button to add start/stop brick
        add_start_stop_btn = Button(text='Add Start/Stop Brick', size_hint_y=None, height='40dp')
        add_start_stop_btn.bind(on_press=lambda x: self.add_brick('start_stop'))
        self.root.add_widget(add_start_stop_btn)

        # Button to add delay brick
        add_delay_btn = Button(text='Add Delay Brick', size_hint_y=None, height='40dp')
        add_delay_btn.bind(on_press=lambda x: self.add_brick('delay'))
        self.root.add_widget(add_delay_btn)

        # Button to load configuration
        load_btn = Button(text='Load Config', size_hint_y=None, height='40dp')
        load_btn.bind(on_press=self.show_load_popup)
        self.root.add_widget(load_btn)

        # Button to save configuration
        save_btn = Button(text='Save Config', size_hint_y=None, height='40dp')
        save_btn.bind(on_press=self.show_save_popup)
        self.root.add_widget(save_btn)

        return self.root

    def add_brick(self, brick_type):
        brick = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        brick.brick_type = brick_type  # Adding type attribute to identify the brick type later

        if brick_type == 'start_stop':
            # Action Spinner
            action_spinner = Spinner(text='Select Action', values=('start', 'stop'), size_hint_x=0.2)
            brick.add_widget(action_spinner)
            action_spinner.widget_type = 'action_spinner'

            # Device Spinner
            device_spinner = Spinner(text='Select Device', values=('Steam', 'Hotwater', 'Vacuum', 'All'), size_hint_x=0.3)
            brick.add_widget(device_spinner)
            device_spinner.widget_type = 'device_spinner'

            # Level Spinner
            level_spinner = Spinner(text='Select Level', values=('Min', 'Med', 'Max'), size_hint_x=0.3)
            brick.add_widget(level_spinner)
            level_spinner.widget_type = 'level_spinner'
        elif brick_type == 'delay':
            # Delay Time Input
            delay_input = TextInput(hint_text='Delay (0-1000)', size_hint_x=0.2, input_filter='int')
            brick.add_widget(delay_input)
            delay_input.widget_type = 'delay_input'

            # Time Type Spinner (Seconds/Minutes)
            time_type_spinner = Spinner(text='Seconds/Minutes', values=('Seconds', 'Minutes'), size_hint_x=0.3)
            brick.add_widget(time_type_spinner)
            time_type_spinner.widget_type = 'time_type_spinner'

            # Blank Field to maintain size consistency
            blank_field = Label(size_hint_x=0.3)
            brick.add_widget(blank_field)

        # Remove Brick Button
        remove_btn = Button(text='Remove', size_hint_x=0.1, size_hint_y=None, height='40dp')
        remove_btn.bind(on_press=lambda x: self.remove_brick(brick))
        brick.add_widget(remove_btn)

        # Move Up Button
        up_btn = Button(text='Up', size_hint_x=0.1, size_hint_y=None, height='40dp')
        up_btn.bind(on_press=lambda x: self.move_brick(brick, 'up'))
        brick.add_widget(up_btn)

        # Move Down Button
        down_btn = Button(text='Down', size_hint_x=0.1, size_hint_y=None, height='40dp')
        down_btn.bind(on_press=lambda x: self.move_brick(brick, 'down'))
        brick.add_widget(down_btn)

        self.brick_container.add_widget(brick)

    def remove_brick(self, brick):
        if self.brick_container:  # Ensure brick_container still exists
            self.brick_container.remove_widget(brick)

    def move_brick(self, brick, direction):
        index = self.brick_container.children.index(brick)
        if direction == 'up' and index < len(self.brick_container.children) - 1:
            self.brick_container.remove_widget(brick)
            self.brick_container.add_widget(brick, index=index + 1)
        elif direction == 'down' and index > 0:
            self.brick_container.remove_widget(brick)
            self.brick_container.add_widget(brick, index=index - 1)

    def show_save_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create buttons for custom filenames
        btn1 = Button(text='Custom Button 1', size_hint_y=None, height='40dp')
        btn2 = Button(text='Custom Button 2', size_hint_y=None, height='40dp')
        btn3 = Button(text='Custom Button 3', size_hint_y=None, height='40dp')

        content.add_widget(btn1)
        content.add_widget(btn2)
        content.add_widget(btn3)

        popup = Popup(title='Save Config', content=content, size_hint=(0.5, 0.5))

        # Bind buttons to save function with predefined filenames
        btn1.bind(on_press=lambda x: self.save_config_file('c1.yaml', popup))
        btn2.bind(on_press=lambda x: self.save_config_file('c2.yaml', popup))
        btn3.bind(on_press=lambda x: self.save_config_file('c3.yaml', popup))

        popup.open()

    def show_load_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        filechooser = FileChooserIconView(path='config', filters=['*.yaml'])
        content.add_widget(filechooser)

        load_btn = Button(text='Load', size_hint_y=None, height='40dp')
        content.add_widget(load_btn)

        popup = Popup(title='Load Config', content=content, size_hint=(0.9, 0.9))
        load_btn.bind(on_press=lambda x: self.load_config_file(filechooser.selection, popup))
        popup.open()

    def load_config_file(self, selection, popup):
        if not selection:
            print("No file selected")
            popup.dismiss()
            return

        filepath = selection[0]

        if not os.path.exists(filepath):
            print(f"Configuration file {filepath} not found")
            popup.dismiss()
            return

        with open(filepath, 'r') as infile:
            config = yaml.safe_load(infile)

        self.brick_container.clear_widgets()  # Clear existing bricks

        for action in config.get('actions', []):
            if action['type'] == 'delay':
                self.add_brick('delay')
                last_brick = self.brick_container.children[0]
                delay_input = next((child for child in last_brick.children if getattr(child, 'widget_type', None) == 'delay_input'), None)
                time_type_spinner = next((child for child in last_brick.children if getattr(child, 'widget_type', None) == 'time_type_spinner'), None)
                if delay_input and time_type_spinner:
                    delay_input.text = str(action['amount'])
                    time_type_spinner.text = 'Seconds' if action['unit'] == 'sec' else 'Minutes'
            elif action['type'] == 'action':
                self.add_brick('start_stop')
                last_brick = self.brick_container.children[0]
                action_spinner = next((child for child in last_brick.children if getattr(child, 'widget_type', None) == 'action_spinner'), None)
                device_spinner = next((child for child in last_brick.children if getattr(child, 'widget_type', None) == 'device_spinner'), None)
                level_spinner = next((child for child in last_brick.children if getattr(child, 'widget_type', None) == 'level_spinner'), None)
                if action_spinner and device_spinner:
                    action_spinner.text = action['action_type'].capitalize()
                    device_spinner.text = action['device']
                    if level_spinner and 'level' in action:
                        level_spinner.text = action['level'].capitalize()

        popup.dismiss()

    def save_config_file(self, filename, popup):
        if not filename.endswith('.yaml'):
            filename += '.yaml'
        if not os.path.exists('config'):
            os.makedirs('config')
        filepath = os.path.join('config', filename)

        config = {'actions': []}

        for brick in self.brick_container.children[::-1]:  # Iterate from top to bottom
            if hasattr(brick, 'brick_type') and brick.brick_type == 'delay':
                delay_input = next((child for child in brick.children if getattr(child, 'widget_type', None) == 'delay_input'), None)
                time_type_spinner = next((child for child in brick.children if getattr(child, 'widget_type', None) == 'time_type_spinner'), None)
                if delay_input and time_type_spinner:
                    delay = delay_input.text
                    time_type = time_type_spinner.text
                    if delay.isdigit():
                        unit = 'sec' if time_type == 'Seconds' else 'min'
                        config['actions'].append({
                            'type': 'delay',
                            'amount': int(delay),
                            'unit': unit
                        })
            elif hasattr(brick, 'brick_type') and brick.brick_type == 'start_stop':
                action_spinner = next((child for child in brick.children if getattr(child, 'widget_type', None) == 'action_spinner'), None)
                device_spinner = next((child for child in brick.children if getattr(child, 'widget_type', None) == 'device_spinner'), None)
                level_spinner = next((child for child in brick.children if getattr(child, 'widget_type', None) == 'level_spinner'), None)
                if action_spinner and device_spinner:
                    action_type = action_spinner.text.lower()
                    device = device_spinner.text.capitalize()
                    level = level_spinner.text.lower() if level_spinner and action_type == 'start' else None
                    action_data = {
                        'type': 'action',
                        'action_type': action_type,
                        'device': device
                    }
                    if level:
                        action_data['level'] = level
                    config['actions'].append(action_data)

        # Save to YAML file
        with open(filepath, 'w') as outfile:
            yaml.dump(config, outfile, default_flow_style=False, sort_keys=False)

        print(f"Configuration saved to {filepath}")
        popup.dismiss()

if __name__ == '__main__':
    ConfigBuilderApp().run()
