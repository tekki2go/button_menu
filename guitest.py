from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.core.window import Window
import yaml
import os

class ConfigBuilderApp(App):
    def build(self):
        Window.size = (1200, 900)  # Set fixed size
        Window.allow_resize = False  # Disallow resizing
        self.root = BoxLayout(orientation='vertical')
        self.brick_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.brick_container.bind(minimum_height=self.brick_container.setter('height'))

        # ScrollView to handle bricks
        scroll = ScrollView(size_hint=(1, 0.7))
        scroll.add_widget(self.brick_container)
        self.root.add_widget(scroll)

        # Button to add start/stop brick
        add_start_stop_btn = Button(text='Add Start/Stop Brick', size_hint=(1, 0.1))
        add_start_stop_btn.bind(on_press=lambda x: self.add_brick('start_stop'))
        self.root.add_widget(add_start_stop_btn)

        # Button to add delay brick
        add_delay_btn = Button(text='Add Delay Brick', size_hint=(1, 0.1))
        add_delay_btn.bind(on_press=lambda x: self.add_brick('delay'))
        self.root.add_widget(add_delay_btn)

        # Button to save configuration
        save_btn = Button(text='Save Config', size_hint=(1, 0.1))
        save_btn.bind(on_press=self.show_save_popup)
        self.root.add_widget(save_btn)

        return self.root

    def add_brick(self, brick_type):
        brick = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')

        if brick_type == 'start_stop':
            # Action Spinner
            action_spinner = Spinner(text='Select Action', values=('start', 'stop'), size_hint_x=0.2)
            brick.add_widget(action_spinner)

            # Device Spinner
            device_spinner = Spinner(text='Select Device', values=('Steam', 'Hotwater', 'Vacuum', 'All'), size_hint_x=0.3)
            brick.add_widget(device_spinner)

            # Level Spinner
            level_spinner = Spinner(text='Select Level', values=('Min', 'Med', 'Max'), size_hint_x=0.3)
            brick.add_widget(level_spinner)
        elif brick_type == 'delay':
            # Delay Time Input
            delay_input = TextInput(hint_text='Delay (0-1000)', size_hint_x=0.2, input_filter='int')
            brick.add_widget(delay_input)

            # Time Type Spinner (Seconds/Minutes)
            time_type_spinner = Spinner(text='Seconds/Minutes', values=('Seconds', 'Minutes'), size_hint_x=0.3)
            brick.add_widget(time_type_spinner)

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
        filename_input = TextInput(hint_text='Enter filename', multiline=False)
        content.add_widget(filename_input)

        save_btn = Button(text='Save', size_hint_y=None, height='40dp')
        content.add_widget(save_btn)

        popup = Popup(title='Save Config', content=content, size_hint=(0.7, 0.5))
        save_btn.bind(on_press=lambda x: self.save_config(filename_input.text, popup))
        popup.open()

    def save_config(self, filename, popup):
        if not filename.endswith('.yaml'):
            filename += '.yaml'
        if not os.path.exists('config'):
            os.makedirs('config')
        filepath = os.path.join('config', filename)

        config = {'actions': {}}
        action_index = 0

        for brick in self.brick_container.children[::-1]:  # Iterate from top to bottom
            if len(brick.children) == 6:  # Delay brick
                delay = brick.children[5].text
                time_type = brick.children[4].text
                if delay.isdigit():
                    unit = 'sec' if time_type == 'Seconds' else 'min'
                    config['actions'][action_index] = {
                        'type': 'delay',
                        'amount': int(delay),
                        'unit': unit
                    }
                    action_index += 1
            elif len(brick.children) == 7:  # Start/Stop brick
                action_type = brick.children[6].text.lower()
                device = brick.children[5].text.lower().capitalize()
                level = brick.children[4].text.lower() if action_type == 'start' else None
                action_data = {
                    'type': 'action',
                    'action_type': action_type,
                    'device': device
                }
                if level:
                    action_data['level'] = level
                config['actions'][action_index] = action_data
                action_index += 1

        # Convert dict to list for correct YAML formatting
        config['actions'] = [config['actions'][key] for key in sorted(config['actions'].keys())]

        # Save to YAML file
        with open(filepath, 'w') as outfile:
            yaml.dump(config, outfile, default_flow_style=False)

        print(f"Configuration saved to {filepath}")
        popup.dismiss()

if __name__ == '__main__':
    ConfigBuilderApp().run()
