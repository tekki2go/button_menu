import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from libs.task_executor import TaskExecutor

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.executor = TaskExecutor()

    def build(self):
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
        try:
            self.executor.execute_from_file(f'config/{config_file}')
            self.show_popup(f'Task from {config_file} executed successfully!')
        except Exception as e:
            self.show_popup(f'Error executing {config_file}: {str(e)}')

    def show_popup(self, message):
        content = BoxLayout(orientation='vertical')
        label = Label(text=message)
        close_button = Button(text="Close", size_hint=(1, 0.2))

        popup = Popup(title='Task Execution', content=content, size_hint=(0.8, 0.4))
        content.add_widget(label)
        content.add_widget(close_button)

        close_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    MainApp().run()
