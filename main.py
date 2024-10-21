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
        self.button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.7))
        self.button_steam = Button(text="STEAM")
        self.button_vacuum = Button(text="VACUUM")
        self.button_extract = Button(text="EXTRACT")
        self.button_layout.add_widget(self.button_steam)
        self.button_layout.add_widget(self.button_vacuum)
        self.button_layout.add_widget(self.button_extract)
        layout.add_widget(self.button_layout)
        
        # Bottom buttons (Menu, Arrow and OFF)
        bottom_layout = BoxLayout(size_hint=(1, 0.2))
        menu_button = Button(text="Menu")
        menu_button.bind(on_press=self.open_menu)
        bottom_layout.add_widget(menu_button)

        arrow_button = Button(text="→")  # Arrow button to go to the extra menu
        arrow_button.bind(on_press=self.open_extra_menu)
        bottom_layout.add_widget(arrow_button)

        off_button = Button(text="OFF")
        bottom_layout.add_widget(off_button)
        layout.add_widget(bottom_layout)
        
        self.add_widget(layout)

    def open_menu(self, instance):
        self.manager.current = 'menu'

    def open_extra_menu(self, instance):
        self.manager.current = 'extra_menu'

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Second menu with 4 options
        button_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8))
        language_button = Button(text="LANGUAGE")
        startup_button = Button(text="STARTUP")
        settings_button = Button(text="SETTINGS")
        settings_button.bind(on_press=self.open_settings)
        maintenance_button = Button(text="MAINTENANCE")
        
        button_layout.add_widget(language_button)
        button_layout.add_widget(startup_button)
        button_layout.add_widget(settings_button)
        button_layout.add_widget(maintenance_button)
        layout.add_widget(button_layout)
        
        # Bottom buttons (Back and OFF)
        bottom_layout = BoxLayout(size_hint=(1, 0.2))
        back_button = Button(text="BACK")
        back_button.bind(on_press=self.go_back)
        bottom_layout.add_widget(back_button)
        
        off_button = Button(text="OFF")
        bottom_layout.add_widget(off_button)
        layout.add_widget(bottom_layout)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'main_menu'

    def open_settings(self, instance):
        self.manager.current = 'settings'

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
        back_button = Button(text="BACK")
        back_button.bind(on_press=self.go_back)
        bottom_layout.add_widget(back_button)
        
        off_button = Button(text="OFF")
        bottom_layout.add_widget(off_button)
        layout.add_widget(bottom_layout)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'menu'

class ExtraMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(ExtraMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Top status bar (Heating: OFF)
        status_bar = BoxLayout(size_hint=(1, 0.1))
        status_bar.add_widget(Label(text="Heating: OFF", size_hint=(1, 0.2)))
        layout.add_widget(status_bar)
        
        # Main buttons (C1, C2, C3)
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.7))
        button_layout.add_widget(Button(text="C1"))
        button_layout.add_widget(Button(text="C2"))
        button_layout.add_widget(Button(text="C3"))
        layout.add_widget(button_layout)
        
        # Bottom buttons (Back and OFF)
        bottom_layout = BoxLayout(size_hint=(1, 0.2))
        back_button = Button(text="BACK")
        back_button.bind(on_press=self.go_back)
        bottom_layout.add_widget(back_button)
        
        off_button = Button(text="OFF")
        bottom_layout.add_widget(off_button)
        layout.add_widget(bottom_layout)
        
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'main_menu'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(ExtraMenuScreen(name='extra_menu'))

        return sm

if __name__ == '__main__':
    MyApp().run()
