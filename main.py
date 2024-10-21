from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.screenmanager import SlideTransition

# Global variable for heating state
heating_state = False

class MainMenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = MDFloatLayout()
        
        # Background color
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)  # #007ae7 color
            RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Heating Rectangle at the top
        with self.canvas:
            Color(0.694, 0.714, 0.788, 1)  # #b1b6c9 color
            RoundedRectangle(
                pos=(Window.width * 0.4, Window.height * 0.92),
                size=(Window.width * 0.2, Window.height * 0.08),
                radius=[(0, 0), (0, 0), (15, 15), (15, 15)]
            )
        
        # Heating label that updates based on the global heating state
        self.heating_label = MDLabel(
            text="Heating: OFF" if not heating_state else "Heating: ON",
            size_hint=(None, None),
            size=(Window.width * 0.2, Window.height * 0.08),
            pos_hint={'center_x': 0.5, 'top': 1},
            color=(0, 0, 0, 1),
            font_style='H5'
        )
        layout.add_widget(self.heating_label)
        
        # Main buttons
        button_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=40
        )

        self.button_steam = MDRectangleFlatButton(
            text="STEAM",
            md_bg_color=(0.008, 0.408, 0.78, 1),
            text_color=(1, 1, 1, 1),
            font_size='24sp',
            size_hint=(1, 1.5)
        )

        self.button_vacuum = MDRectangleFlatButton(
            text="VACUUM",
            md_bg_color=(0.008, 0.408, 0.78, 1),
            text_color=(1, 1, 1, 1),
            font_size='24sp',
            size_hint=(1, 1.5)
        )

        self.button_extract = MDRectangleFlatButton(
            text="EXTRACT",
            md_bg_color=(0.008, 0.408, 0.78, 1),
            text_color=(1, 1, 1, 1),
            font_size='24sp',
            size_hint=(1, 1.5)
        )

        button_layout.add_widget(self.button_steam)
        button_layout.add_widget(self.button_vacuum)
        button_layout.add_widget(self.button_extract)
        layout.add_widget(button_layout)
        
        # Bottom buttons (Menu, Off, and Custom)
        bottom_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            pos_hint={'y': 0}
        )
        menu_button = MDRaisedButton(
            text="Menu",
            md_bg_color=(0.008, 0.408, 0.78, 1),
            text_color=(1, 1, 1, 1),
            font_size='20sp'
        )
        menu_button.bind(on_press=self.open_menu)
        bottom_layout.add_widget(menu_button)
        
        off_button = MDRaisedButton(
            text="Off",
            md_bg_color=(0.008, 0.408, 0.78, 1),
            text_color=(1, 1, 1, 1),
            font_size='20sp'
        )
        off_button.bind(on_press=self.shutdown_sequence)
        bottom_layout.add_widget(off_button)
        
        arrow_button = MDRaisedButton(
            text="Custom",
            md_bg_color=(0.008, 0.408, 0.78, 1),
            text_color=(1, 1, 1, 1),
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
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)  # #007ae7 color
            RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Display shutdown message with countdown
        self.countdown_label = MDLabel(
            text="Shutting down in 5",
            font_style='H5',
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
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
            MDApp.get_running_app().stop()
            Window.close()

class MenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        
        # Second menu with 4 options
        button_layout = MDBoxLayout(orientation='vertical', size_hint=(1, 0.8))
        language_button = MDRaisedButton(text="LANGUAGE", font_size='20sp')
        startup_button = MDRaisedButton(text="STARTUP", font_size='20sp')
        settings_button = MDRaisedButton(text="SETTINGS", font_size='20sp')
        settings_button.bind(on_press=self.open_settings)
        maintenance_button = MDRaisedButton(text="MAINTENANCE", font_size='20sp')
        
        button_layout.add_widget(language_button)
        button_layout.add_widget(startup_button)
        button_layout.add_widget(settings_button)
        button_layout.add_widget(maintenance_button)
        layout.add_widget(button_layout)
        
        # Bottom buttons (Back and OFF)
        bottom_layout = MDBoxLayout(size_hint=(1, 0.2))
        back_button = MDRaisedButton(text="BACK", font_size='20sp')
        back_button.bind(on_press=self.go_back)
        bottom_layout.add_widget(back_button)
        
        off_button = MDRaisedButton(text="OFF", font_size='20sp')
        off_button.bind(on_press=self.shutdown_sequence)
        bottom_layout.add_widget(off_button)
        layout.add_widget(bottom_layout)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="down")
        self.manager.current = 'main_menu'

    def open_settings(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'settings'

    def shutdown_sequence(self, instance):
        self.clear_widgets()
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)  # #007ae7 color
            RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Display shutdown message with countdown
        self.countdown_label = MDLabel(text="Shutting down in 5", font_style='H5', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.countdown_label)
        
        # Start countdown
        self.countdown = 5
        Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        self.countdown -= 1
        if self.countdown > 0:
            self.countdown_label.text = f"Shutting down in {self.countdown}"
        else:
            MDApp.get_running_app().stop()
            Window.close()

class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        
        # Settings list with options
        button_layout = MDBoxLayout(orientation='vertical', size_hint=(1, 0.8))
        button_layout.add_widget(MDRaisedButton(text="Standby: 120 min", font_size='20sp'))
        button_layout.add_widget(MDRaisedButton(text="Screen Brightness: 100%", font_size='20sp'))
        button_layout.add_widget(MDRaisedButton(text="Bluetooth", font_size='20sp'))
        button_layout.add_widget(MDRaisedButton(text="Wi-Fi", font_size='20sp'))
        layout.add_widget(button_layout)
        
        # Bottom buttons (Back and OFF)
        bottom_layout = MDBoxLayout(size_hint=(1, 0.2))
        back_button = MDRaisedButton(text="BACK", font_size='20sp')
        back_button.bind(on_press=self.go_back)
        bottom_layout.add_widget(back_button)
        
        off_button = MDRaisedButton(text="OFF", font_size='20sp')
        off_button.bind(on_press=self.shutdown_sequence)
        bottom_layout.add_widget(off_button)
        layout.add_widget(bottom_layout)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'menu'

    def shutdown_sequence(self, instance):
        self.clear_widgets()
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)  # #007ae7 color
            RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Display shutdown message with countdown
        self.countdown_label = MDLabel(text="Shutting down in 5", font_style='H5', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.countdown_label)
        
        # Start countdown
        self.countdown = 5
        Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        self.countdown -= 1
        if self.countdown > 0:
            self.countdown_label.text = f"Shutting down in {self.countdown}"
        else:
            MDApp.get_running_app().stop()
            Window.close()

class ExtraMenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super(ExtraMenuScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        
        # Top status bar (Heating: OFF)
        status_bar = MDBoxLayout(size_hint=(1, 0.1))
        status_bar.add_widget(MDLabel(text="Heating: OFF", size_hint=(1, 0.2), font_style='H5'))
        layout.add_widget(status_bar)
        
        # Main buttons (C1, C2, C3)
        button_layout = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.7))
        button_layout.add_widget(MDRaisedButton(text="C1", font_size='20sp'))
        button_layout.add_widget(MDRaisedButton(text="C2", font_size='20sp'))
        button_layout.add_widget(MDRaisedButton(text="C3", font_size='20sp'))
        layout.add_widget(button_layout)
        
        # Bottom buttons (Back and OFF)
        bottom_layout = MDBoxLayout(size_hint=(1, 0.2))
        back_button = MDRaisedButton(text="BACK", font_size='20sp')
        back_button.bind(on_press=self.go_back)
        bottom_layout.add_widget(back_button)
        
        off_button = MDRaisedButton(text="OFF", font_size='20sp')
        off_button.bind(on_press=self.shutdown_sequence)
        bottom_layout.add_widget(off_button)
        layout.add_widget(bottom_layout)
        
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'main_menu'

    def shutdown_sequence(self, instance):
        self.clear_widgets()
        with self.canvas.before:
            Color(0, 0.478, 0.905, 1)  # #007ae7 color
            RoundedRectangle(pos=self.pos, size=Window.size)
        
        # Display shutdown message with countdown
        self.countdown_label = MDLabel(text="Shutting down in 5", font_style='H5', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.countdown_label)
        
        # Start countdown
        self.countdown = 5
        Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        self.countdown -= 1
        if self.countdown > 0:
            self.countdown_label.text = f"Shutting down in {self.countdown}"
        else:
            MDApp.get_running_app().stop()
            Window.close()

class MyApp(MDApp):
    def build(self):
        sm = MDScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(ExtraMenuScreen(name='extra_menu'))

        return sm

if __name__ == '__main__':
    MyApp().run()
