from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import threading


class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main container
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        layout.add_widget(MDLabel(
            text="Load Tester",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=50
        ))
        
        # URL Input
        self.url_input = MDTextField(
            hint_text="Target URL",
            text="https://example.com",
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.url_input)
        
        # Requests Input
        self.requests_input = MDTextField(
            hint_text="Requests",
            text="100",
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.requests_input)
        
        # Start Button
        self.btn = MDRaisedButton(
            text="START",
            size_hint=(1, None),
            height=50,
            on_release=self.start_test
        )
        layout.add_widget(self.btn)
        
        # Output
        scroll = ScrollView(size_hint=(1, 0.5))
        self.output = MDLabel(
            text="Ready...",
            size_hint_y=None
        )
        self.output.bind(texture_size=self.output.setter('size'))
        scroll.add_widget(self.output)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def start_test(self, instance):
        self.output.text = f"Testing {self.url_input.text}...\nRequests: {self.requests_input.text}"
        self.btn.disabled = True
        
        # Run test in background
        threading.Thread(target=self.run_test, daemon=True).start()
    
    def run_test(self):
        import requests
        url = self.url_input.text
        count = int(self.requests_input.text)
        
        success = 0
        failed = 0
        
        for i in range(count):
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    success += 1
                else:
                    failed += 1
            except:
                failed += 1
            
            if i % 10 == 0:
                Clock.schedule_once(lambda dt: self.update_output(i+1, success, failed), 0)
        
        Clock.schedule_once(lambda dt: self.test_done(success, failed), 0)
    
    def update_output(self, current, success, failed):
        self.output.text = f"Progress: {current}\nSuccess: {success}\nFailed: {failed}"
    
    def test_done(self, success, failed):
        self.output.text = f"DONE!\n\nSuccess: {success}\nFailed: {failed}"
        self.btn.disabled = False


class LoadTesterApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return MainScreen()
    
    def on_start(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.INTERNET])
        except:
            pass


if __name__ == '__main__':
    LoadTesterApp().run()
