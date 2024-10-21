from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Top status bar (Heating: OFF)
        status_bar = BoxLayout(size_hint=(1, 0.1))
        status_bar.add_widget(Label(text="Heating: OFF", size_hint=(1, 0.2)))
        layout.add_widget(status_bar)
        
        # Main buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.7))
        button_layout.add_widget(Button(text="STEAM"))
        button_layout.add_widget(Button(text="VACUUM"))
        button_layout.add_widget(Button(text="EXTRACT"))
        layout.add_widget(button_layout)
        
        # Bottom buttons (Menu and OFF)
        bottom_layout = BoxLayout(size_hint=(1, 0.2))
        bottom_layout.add_widget(Button(text="Menu"))
        bottom_layout.add_widget(Button(text="OFF"))
        layout.add_widget(bottom_layout)
        
        self.add_widget(layout)

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Second menu with 4 options
        button_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8))
        button_layout.add_widget(Button(text="LANGUAGE"))
        button_layout.add_widget(Button(text="STARTUP"))
        button_layout.add_widget(Button(text="SETTINGS"))
        button_layout.add_widget(Button(text="MAINTENANCE"))
        layout.add_widget(button_layout)
        
        # Bottom buttons (Back and OFF)
        bottom_layout = BoxLayout(size_hint=(1, 0.2))
        bottom_layout.add_widget(Button(text="BACK"))
        bottom_layout.add_widget(Button(text="OFF"))
        layout.add_widget(bottom_layout)

        self.add_widget(layout)

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Settings list with options
        button_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8))
        button_layout.add_widget(Button(text="Standby: 120 min"))
        button_layout.add_widget(Button(text="Screen Brightness: 100%"))
        button_layout.add_widget(Button(text="Bluetooth"))
        button_layout.add_widget(Button(text="Wi-Fi"))
        layout.add_widget(button_layout)
        
        # Bottom buttons (Back and OFF)
        bottom_layout = BoxLayout(size_hint=(1, 0.2))
        bottom_layout.add_widget(Button(text="BACK"))
        bottom_layout.add_widget(Button(text="OFF"))
        layout.add_widget(bottom_layout)

        self.add_widget(layout)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm

if __name__ == '__main__':
    MyApp().run()
