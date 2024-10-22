from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window
from kivy.clock import Clock
import yaml
import os

# Global variable for heating state
heating_state = False

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        
        # Background color
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)  # #007ae7 color
            self.bg_rect = RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Heating Rectangle at the top
        with self.canvas:
            Color(0.694, 0.714, 0.788, 1)  # #b1b6c9 color
            self.heating_rect = RoundedRectangle(
                pos=(Window.width * 0.4, Window.height * 0.92),
                size=(Window.width * 0.2, Window.height * 0.08),
                radius=[(0, 0), (0, 0), (15, 15), (15, 15)]
            )
        
        # Heating label that updates based on the global heating state
        self.heating_label = Label(
            text="Heating: OFF" if not heating_state else "Heating: ON",
            size_hint=(None, None),
            size=(Window.width * 0.2, Window.height * 0.08),
            pos_hint={'center_x': 0.5, 'top': 1},
            color=(0, 0, 0, 1),
            font_size='24sp'
        )
        layout.add_widget(self.heating_label)
        
        # Main buttons
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=40
        )
        
        self.button_steam = Button(
            text="STEAM",
            background_color=(0.008, 0.408, 0.78, 1),
            color=(1, 1, 1, 1),
            font_size='24sp',
            background_normal='',
            background_down=''
        )

        self.button_vacuum = Button(
            text="VACUUM",
            background_color=(0.008, 0.408, 0.78, 1),
            color=(1, 1, 1, 1),
            font_size='24sp',
            background_normal='',
            background_down=''
        )

        self.button_extract = Button(
            text="EXTRACT",
            background_color=(0.008, 0.408, 0.78, 1),
            color=(1, 1, 1, 1),
            font_size='24sp',
            background_normal='',
            background_down=''
        )

        button_layout.add_widget(self.button_steam)
        button_layout.add_widget(self.button_vacuum)
        button_layout.add_widget(self.button_extract)
        layout.add_widget(button_layout)
        
        # Bottom buttons (Menu, Off, and Custom)
        bottom_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            pos_hint={'y': 0},
            spacing=10,
            padding=[10, 0, 10, 10]
        )
        menu_button = Button(
            text="Menu",
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            background_down='',
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        menu_button.bind(on_press=self.open_menu)
        bottom_layout.add_widget(menu_button)
        
        off_button = Button(
            text="Off",
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            background_down='',
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        off_button.bind(on_press=self.shutdown_sequence)
        bottom_layout.add_widget(off_button)
        
        arrow_button = Button(
            text="Custom",
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            background_down='',
            color=(1, 1, 1, 1),
            font_size='20sp'
        )  # Custom button to go to the extra menu
        arrow_button.bind(on_press=self.open_extra_menu)
        bottom_layout.add_widget(arrow_button)
        
        layout.add_widget(bottom_layout)
        
        self.add_widget(layout)

        # Schedule heating label updates
        Clock.schedule_interval(self.update_heating_label, 1)

    def update_heating_label(self, dt):
        self.heating_label.text = "Heating: OFF" if not heating_state else "Heating: ON"

    def open_menu(self, instance):
        self.manager.transition = SlideTransition(direction="up")
        self.manager.current = 'menu'

    def open_extra_menu(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'extra_menu'

    def shutdown_sequence(self, instance):
        # Clear the screen except for the background
        self.clear_widgets()
        self.canvas.clear()
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)  # #007ae7 color
            self.bg_rect = RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Display shutdown message with border
        with self.canvas:
            Color(1, 1, 1, 1)
            self.shutdown_rect = RoundedRectangle(
                size=(Window.width * 0.6, Window.height * 0.2),
                pos=(Window.width * 0.2, Window.height * 0.4),
                radius=[20]
            )
            Color(0, 0, 0, 1)
            Line(
                rounded_rectangle=(
                    Window.width * 0.2, Window.height * 0.4,
                    Window.width * 0.6, Window.height * 0.2, 20
                ),
                width=2
            )
        
        self.countdown_label = Label(
            text="Shutting down in 5",
            font_size='30sp',
            size_hint=(None, None),
            size=(Window.width * 0.6, Window.height * 0.2),
            pos=(Window.width * 0.2, Window.height * 0.4),
            color=(0, 0, 0, 1)
        )
        self.add_widget(self.countdown_label)
        
        # Start countdown
        self.countdown = 5
        Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        self.countdown -= 1
        if self.countdown > 0:
            self.countdown_label.text = f"Shutting down in {self.countdown}"
        else:
            App.get_running_app().stop()
            Window.close()

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        
        # Background color
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)  # #007ae7 color
            self.bg_rect = RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Heating Rectangle at the top
        with self.canvas:
            Color(0.694, 0.714, 0.788, 1)  # #b1b6c9 color
            self.heating_rect = RoundedRectangle(
                pos=(Window.width * 0.4, Window.height * 0.92),
                size=(Window.width * 0.2, Window.height * 0.08),
                radius=[(0, 0), (0, 0), (15, 15), (15, 15)]
            )
        
        # Heating label
        self.heating_label = Label(
            text="Heating: OFF" if not heating_state else "Heating: ON",
            size_hint=(None, None),
            size=(Window.width * 0.2, Window.height * 0.08),
            pos_hint={'center_x': 0.5, 'top': 1},
            color=(0, 0, 0, 1),
            font_size='24sp'
        )
        layout.add_widget(self.heating_label)
        
        # Second menu with 4 options
        button_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=20
        )
        language_button = Button(
            text="LANGUAGE",
            font_size='24sp',
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        startup_button = Button(
            text="STARTUP",
            font_size='24sp',
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        settings_button = Button(
            text="SETTINGS",
            font_size='24sp',
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        settings_button.bind(on_press=self.open_settings)
        maintenance_button = Button(
            text="MAINTENANCE",
            font_size='24sp',
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        
        button_layout.add_widget(language_button)
        button_layout.add_widget(startup_button)
        button_layout.add_widget(settings_button)
        button_layout.add_widget(maintenance_button)
        layout.add_widget(button_layout)
        
        # Bottom buttons (Back and OFF) with spacing and padding
        bottom_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            pos_hint={'y': 0},
            spacing=10,
            padding=[10, 0, 10, 10]
        )
        back_button = Button(
            text="BACK",
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            background_down='',
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        back_button.bind(on_press=self.go_back)
        bottom_layout.add_widget(back_button)
        
        off_button = Button(
            text="OFF",
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            background_down='',
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        off_button.bind(on_press=self.shutdown_sequence)
        bottom_layout.add_widget(off_button)
        layout.add_widget(bottom_layout)
    
        self.add_widget(layout)

        # Schedule heating label updates
        Clock.schedule_interval(self.update_heating_label, 1)
    
    def update_heating_label(self, dt):
        self.heating_label.text = "Heating: OFF" if not heating_state else "Heating: ON"
    
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="down")
        self.manager.current = 'main_menu'
    
    def open_settings(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'settings'
    
    def shutdown_sequence(self, instance):
        self.clear_widgets()
        self.canvas.clear()
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Display shutdown message with border
        with self.canvas:
            Color(1, 1, 1, 1)
            self.shutdown_rect = RoundedRectangle(
                size=(Window.width * 0.6, Window.height * 0.2),
                pos=(Window.width * 0.2, Window.height * 0.4),
                radius=[20]
            )
            Color(0, 0, 0, 1)
            Line(
                rounded_rectangle=(
                    Window.width * 0.2, Window.height * 0.4,
                    Window.width * 0.6, Window.height * 0.2, 20
                ),
                width=2
            )
        
        self.countdown_label = Label(
            text="Shutting down in 5",
            font_size='30sp',
            size_hint=(None, None),
            size=(Window.width * 0.6, Window.height * 0.2),
            pos=(Window.width * 0.2, Window.height * 0.4),
            color=(0, 0, 0, 1)
        )
        self.add_widget(self.countdown_label)
        
        self.countdown = 5
        Clock.schedule_interval(self.update_countdown, 1)
    
    def update_countdown(self, dt):
        self.countdown -= 1
        if self.countdown > 0:
            self.countdown_label.text = f"Shutting down in {self.countdown}"
        else:
            App.get_running_app().stop()
            Window.close()

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        
        # Background color
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Heating Rectangle at the top
        with self.canvas:
            Color(0.694, 0.714, 0.788, 1)
            self.heating_rect = RoundedRectangle(
                pos=(Window.width * 0.4, Window.height * 0.92),
                size=(Window.width * 0.2, Window.height * 0.08),
                radius=[(0, 0), (0, 0), (15, 15), (15, 15)]
            )
        
        # Heating label
        self.heating_label = Label(
            text="Heating: OFF" if not heating_state else "Heating: ON",
            size_hint=(None, None),
            size=(Window.width * 0.2, Window.height * 0.08),
            pos_hint={'center_x': 0.5, 'top': 1},
            color=(0, 0, 0, 1),
            font_size='24sp'
        )
        layout.add_widget(self.heating_label)
        
        # Settings list with options
        button_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=20
        )
        button_layout.add_widget(Button(
            text="Standby: 120 min",
            font_size='24sp',
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        ))
        button_layout.add_widget(Button(
            text="Screen Brightness: 100%",
            font_size='24sp',
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        ))
        button_layout.add_widget(Button(
            text="Bluetooth",
            font_size='24sp',
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        ))
        button_layout.add_widget(Button(
            text="Wi-Fi",
            font_size='24sp',
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        ))
        layout.add_widget(button_layout)
        
        # Bottom buttons (Back and OFF) with spacing and padding
        bottom_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            pos_hint={'y': 0},
            spacing=10,
            padding=[10, 0, 10, 10]
        )
        back_button = Button(
            text="BACK",
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            background_down='',
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        back_button.bind(on_press=self.go_back)
        bottom_layout.add_widget(back_button)
        
        off_button = Button(
            text="OFF",
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            background_down='',
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        off_button.bind(on_press=self.shutdown_sequence)
        bottom_layout.add_widget(off_button)
        layout.add_widget(bottom_layout)
    
        self.add_widget(layout)

        # Schedule heating label updates
        Clock.schedule_interval(self.update_heating_label, 1)
    
    def update_heating_label(self, dt):
        self.heating_label.text = "Heating: OFF" if not heating_state else "Heating: ON"
    
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'menu'
    
    def shutdown_sequence(self, instance):
        self.clear_widgets()
        self.canvas.clear()
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Display shutdown message with border
        with self.canvas:
            Color(1, 1, 1, 1)
            self.shutdown_rect = RoundedRectangle(
                size=(Window.width * 0.6, Window.height * 0.2),
                pos=(Window.width * 0.2, Window.height * 0.4),
                radius=[20]
            )
            Color(0, 0, 0, 1)
            Line(
                rounded_rectangle=(
                    Window.width * 0.2, Window.height * 0.4,
                    Window.width * 0.6, Window.height * 0.2, 20
                ),
                width=2
            )
        
        self.countdown_label = Label(
            text="Shutting down in 5",
            font_size='30sp',
            size_hint=(None, None),
            size=(Window.width * 0.6, Window.height * 0.2),
            pos=(Window.width * 0.2, Window.height * 0.4),
            color=(0, 0, 0, 1)
        )
        self.add_widget(self.countdown_label)
        
        self.countdown = 5
        Clock.schedule_interval(self.update_countdown, 1)
    
    def update_countdown(self, dt):
        self.countdown -= 1
        if self.countdown > 0:
            self.countdown_label.text = f"Shutting down in {self.countdown}"
        else:
            App.get_running_app().stop()
            Window.close()

class ExtraMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(ExtraMenuScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        
        # Load actions from YAML files
        self.load_actions()
        
        # Background color
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Heating Rectangle at the top
        with self.canvas:
            Color(0.694, 0.714, 0.788, 1)
            self.heating_rect = RoundedRectangle(
                pos=(Window.width * 0.4, Window.height * 0.92),
                size=(Window.width * 0.2, Window.height * 0.08),
                radius=[(0, 0), (0, 0), (15, 15), (15, 15)]
            )
        
        # Heating label
        self.heating_label = Label(
            text="Heating: OFF" if not heating_state else "Heating: ON",
            size_hint=(None, None),
            size=(Window.width * 0.2, Window.height * 0.08),
            pos_hint={'center_x': 0.5, 'top': 1},
            color=(0, 0, 0, 1),
            font_size='24sp'
        )
        layout.add_widget(self.heating_label)
        
        # Main buttons (C1, C2, C3)
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=40
        )
        self.button_c1 = Button(
            text="C1",
            font_size='24sp',
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        self.button_c2 = Button(
            text="C2",
            font_size='24sp',
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        self.button_c3 = Button(
            text="C3",
            font_size='24sp',
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        button_layout.add_widget(self.button_c1)
        button_layout.add_widget(self.button_c2)
        button_layout.add_widget(self.button_c3)
        layout.add_widget(button_layout)
        
        # Bottom buttons (Back, OFF, and SHOW ACTIONS)
        bottom_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            pos_hint={'y': 0},
            spacing=10,
            padding=[10, 0, 10, 10]
        )
        back_button = Button(
            text="BACK",
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            background_down='',
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        back_button.bind(on_press=self.go_back)
        bottom_layout.add_widget(back_button)
        
        off_button = Button(
            text="OFF",
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            background_down='',
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        off_button.bind(on_press=self.shutdown_sequence)
        bottom_layout.add_widget(off_button)
        
        show_actions_button = Button(
            text="SHOW ACTIONS",
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            background_down='',
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        show_actions_button.bind(on_press=self.show_actions)
        bottom_layout.add_widget(show_actions_button)
        layout.add_widget(bottom_layout)
    
        self.add_widget(layout)
    
        # Schedule heating label updates
        Clock.schedule_interval(self.update_heating_label, 1)
    
    def load_actions(self):
        self.button_actions = {}
        config_dir = 'config'
        for i in range(1, 4):
            filename = f'c{i}.yaml'
            filepath = os.path.join(config_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as file:
                    data = yaml.safe_load(file)
                    self.button_actions[f'C{i}'] = data.get('actions', [])
            else:
                self.button_actions[f'C{i}'] = []
    
    def update_heating_label(self, dt):
        self.heating_label.text = "Heating: OFF" if not heating_state else "Heating: ON"
    
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'main_menu'
    
    def shutdown_sequence(self, instance):
        self.clear_widgets()
        self.canvas.clear()
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Display shutdown message with border
        with self.canvas:
            Color(1, 1, 1, 1)
            self.shutdown_rect = RoundedRectangle(
                size=(Window.width * 0.6, Window.height * 0.2),
                pos=(Window.width * 0.2, Window.height * 0.4),
                radius=[20]
            )
            Color(0, 0, 0, 1)
            Line(
                rounded_rectangle=(
                    Window.width * 0.2, Window.height * 0.4,
                    Window.width * 0.6, Window.height * 0.2, 20
                ),
                width=2
            )
        
        self.countdown_label = Label(
            text="Shutting down in 5",
            font_size='30sp',
            size_hint=(None, None),
            size=(Window.width * 0.6, Window.height * 0.2),
            pos=(Window.width * 0.2, Window.height * 0.4),
            color=(0, 0, 0, 1)
        )
        self.add_widget(self.countdown_label)
        
        self.countdown = 5
        Clock.schedule_interval(self.update_countdown, 1)
    
    def update_countdown(self, dt):
        self.countdown -= 1
        if self.countdown > 0:
            self.countdown_label.text = f"Shutting down in {self.countdown}"
        else:
            App.get_running_app().stop()
            Window.close()
    
    def show_actions(self, instance):
        # Navigate to ShowActionsScreen
        self.manager.transition = SlideTransition(direction="left")
        if not self.manager.has_screen('show_actions'):
            self.manager.add_widget(ShowActionsScreen(self.button_actions, name='show_actions'))
        self.manager.current = 'show_actions'

class ShowActionsScreen(Screen):
    def __init__(self, button_actions, **kwargs):
        super(ShowActionsScreen, self).__init__(**kwargs)
        self.button_actions = button_actions
        
        layout = FloatLayout()
        
        # Background color
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Scrollable area for actions
        scroll_view = ScrollView(
            size_hint=(1, 0.85),
            pos_hint={'x': 0, 'top': 0.95}
        )
        content = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10,
            padding=10
        )
        content.bind(minimum_height=content.setter('height'))
        
        for button_name in sorted(self.button_actions.keys()):
            actions = self.button_actions[button_name]
            # Display button name
            button_label = Label(
                text=f"[b]{button_name} Actions:[/b]",
                markup=True,
                font_size='24sp',
                size_hint_y=None,
                height=40,
                color=(1, 1, 1, 1)
            )
            content.add_widget(button_label)
            # Display actions
            for action in actions:
                action_text = self.parse_action(action)
                action_label = Label(
                    text=action_text,
                    font_size='20sp',
                    size_hint_y=None,
                    height=30,
                    color=(1, 1, 1, 1)
                )
                content.add_widget(action_label)
            # Add a separator
            separator = Label(
                text="",
                size_hint_y=None,
                height=20
            )
            content.add_widget(separator)
        
        scroll_view.add_widget(content)
        layout.add_widget(scroll_view)
        
        # Bottom buttons (Back)
        bottom_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            pos_hint={'y': 0},
            padding=[10, 0, 10, 10]
        )
        back_button = Button(
            text="BACK",
            background_color=(0.008, 0.408, 0.78, 1),
            background_normal='',
            background_down='',
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        back_button.bind(on_press=self.go_back)
        bottom_layout.add_widget(back_button)
        layout.add_widget(bottom_layout)
        
        self.add_widget(layout)
    
    def parse_action(self, action):
        action_type = action.get('type', '').capitalize()
        if action_type == 'Start':
            device = action.get('device', 'Unknown')
            level = action.get('level', 'Unknown')
            return f"Start {device} at {level} level."
        elif action_type == 'Stop':
            device = action.get('device', 'Unknown')
            return f"Stop {device}."
        elif action_type == 'Delay':
            amount = action.get('amount', 'Unknown')
            unit = action.get('unit', 'Unknown')
            return f"Delay for {amount} {unit}."
        else:
            return "Unknown action."
    
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'extra_menu'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(ExtraMenuScreen(name='extra_menu'))
        # Note: ShowActionsScreen is added dynamically when needed

        return sm

if __name__ == '__main__':
    MyApp().run()
