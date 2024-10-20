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
from kivy_garden.drag_n_drop import DraggableObjectBehavior
from kivy.clock import Clock
import yaml
import os

class DraggableBox(DraggableObjectBehavior, BoxLayout):
    def on_touch_move(self, touch):
        # Make the box follow the touch movement
        if self.collide_point(*touch.pos):
            self.center_x = touch.x
            self.center_y = touch.y
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        # On release, reorder the box in the container
        super().on_touch_up(touch)
        if self.collide_point(*touch.pos) and self.parent:
            Clock.schedule_once(self.reorder_siblings)

    def reorder_siblings(self, *args):
        siblings = list(self.parent.children)
        siblings.remove(self)
        # Calculate the new position based on touch location
        for i, sibling in enumerate(siblings):
            if self.top > sibling.top:
                siblings.insert(i, self)
                break
        else:
            siblings.append(self)
        self.parent.clear_widgets()
        for widget in siblings:
            self.parent.add_widget(widget)

class ConfigBuilderApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        self.brick_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.brick_container.bind(minimum_height=self.brick_container.setter('height'))

        # ScrollView to handle bricks
        scroll = ScrollView(size_hint=(1, 0.7))
        scroll.add_widget(self.brick_container)
        self.root.add_widget(scroll)

        # Button to add bricks
        add_brick_btn = Button(text='Add Brick', size_hint=(1, 0.1))
        add_brick_btn.bind(on_press=self.add_brick)
        self.root.add_widget(add_brick_btn)

        # Button to save configuration
        save_btn = Button(text='Save Config', size_hint=(1, 0.1))
        save_btn.bind(on_press=self.save_config)
        self.root.add_widget(save_btn)

        # Filename selection
        self.filename_spinner = Spinner(text='Select Filename', values=('c1.yaml', 'c2.yaml', 'c3.yaml'), size_hint=(1, 0.1))
        self.root.add_widget(self.filename_spinner)

        return self.root

    def add_brick(self, instance):
        brick = DraggableBox(orientation='horizontal', size_hint_y=None, height='40dp')

        # Action Spinner
        action_spinner = Spinner(text='Select Action', values=('start', 'stop', 'delay'), size_hint_x=0.15)
        action_spinner.bind(text=self.update_brick_visibility)
        brick.add_widget(action_spinner)

        # Device Spinner
        device_spinner = Spinner(text='Select Device', values=('Steam', 'Hotwater', 'Vacuum'), size_hint_x=0.15)
        brick.add_widget(device_spinner)

        # Level Spinner
        level_spinner = Spinner(text='Select Level', values=('Min', 'Med', 'Max'), size_hint_x=0.15)
        brick.add_widget(level_spinner)

        # Delay TextInput
        delay_input = TextInput(hint_text='Delay (0-1000s/m)', size_hint_x=0.15, input_filter='int')
        brick.add_widget(delay_input)

        # Time Type Spinner (Seconds/Minutes)
        time_type_spinner = Spinner(text='Seconds/Minutes', values=('Seconds', 'Minutes'), size_hint_x=0.15)
        brick.add_widget(time_type_spinner)

        # Remove Brick Button
        remove_btn = Button(text='Remove', size_hint_x=0.1)
        remove_btn.bind(on_press=lambda x: self.remove_brick(brick))
        brick.add_widget(remove_btn)

        self.brick_container.add_widget(brick)

    def remove_brick(self, brick):
        if self.brick_container:  # Ensure brick_container still exists
            self.brick_container.remove_widget(brick)

    def update_brick_visibility(self, spinner, text):
        brick = spinner.parent
        if brick is not None:
            if text == 'delay':
                brick.children[4].disabled = True  # Device Spinner
                brick.children[3].disabled = True  # Level Spinner
                brick.children[2].disabled = False  # Delay Input
            elif text in ('start', 'stop'):
                brick.children[4].disabled = False  # Device Spinner
                brick.children[3].disabled = (text == 'stop')  # Level Spinner
                brick.children[2].disabled = True  # Delay Input

    def save_config(self, instance):
        config = {}
        config['c1'] = []

        for brick in self.brick_container.children[::-1]:  # Iterate from top to bottom
            action = brick.children[5].text
            device = brick.children[4].text
            level = brick.children[3].text
            delay = brick.children[2].text
            time_type = brick.children[1].text

            if action == 'delay':
                if delay:
                    time_suffix = 's' if time_type == 'Seconds' else 'm'
                    config['c1'].append({'delay': f"{delay}{time_suffix}"})
            elif action == 'start':
                if action and device and level:
                    config['c1'].append({
                        'action': action,
                        'device': device,
                        'level': level.lower()
                    })
            elif action == 'stop':
                if action and device:
                    config['c1'].append({
                        'action': action,
                        'device': device
                    })

        # Save to YAML file
        if not os.path.exists('config'):
            os.makedirs('config')
        filename = self.filename_spinner.text
        filepath = os.path.join('config', filename)
        with open(filepath, 'w') as outfile:
            yaml.dump(config, outfile, default_flow_style=False)

        print(f"Configuration saved to {filepath}")

if __name__ == '__main__':
    ConfigBuilderApp().run()
