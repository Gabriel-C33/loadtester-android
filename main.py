from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.switch import MDSwitch
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
import threading
import json
import os
import sys
from datetime import datetime
from io import StringIO

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_tester = None
        self.is_running = False
        self.stats_update_event = None
        
        # Layout
        self.padding = [20, 20, 20, 20]
        
        # Title
        self.title_label = MDLabel(
            text="Load Tester",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=60,
            pos_hint={"center_x": 0.5}
        )
        self.add_widget(self.title_label)
        
        # URL Input
        self.url_input = MDTextField(
            hint_text="Target URL",
            text="https://pgisliven.eu",
            size_hint_y=None,
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.85}
        )
        self.add_widget(self.url_input)
        
        # Requests Input
        self.requests_input = MDTextField(
            hint_text="Number of Requests",
            text="1000",
            input_filter="int",
            size_hint_y=None,
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.75}
        )
        self.add_widget(self.requests_input)
        
        # Threads Input
        self.threads_input = MDTextField(
            hint_text="Concurrent Threads",
            text="50",
            input_filter="int",
            size_hint_y=None,
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.65}
        )
        self.add_widget(self.threads_input)
        
        # Start/Stop Button
        self.control_button = MDRaisedButton(
            text="START TEST",
            size_hint=(0.8, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.55},
            on_release=self.toggle_test
        )
        self.add_widget(self.control_button)
        
        # Stats Display (Scrollable)
        self.stats_scroll = ScrollView(
            size_hint=(1, 0.4),
            pos_hint={"center_x": 0.5, "top": 0.45}
        )
        
        self.stats_label = MDLabel(
            text="Ready to start...",
            size_hint_y=None,
            markup=True
        )
        self.stats_label.bind(texture_size=self.stats_label.setter('size'))
        
        self.stats_scroll.add_widget(self.stats_label)
        self.add_widget(self.stats_scroll)
        
        # Load saved data
        self.load_saved_data()
    
    def toggle_test(self, instance):
        if not self.is_running:
            self.start_test()
        else:
            self.stop_test()
    
    def start_test(self):
        try:
            url = self.url_input.text.strip()
            requests = int(self.requests_input.text)
            threads = int(self.threads_input.text)
            
            if not url:
                self.show_dialog("Error", "Please enter a valid URL")
                return
            
            # Create load tester instance
            self.load_tester = LoadTester(
                url=url,
                request_num=requests,
                concurrent_threads=threads,
                callback=self.update_stats
            )
            
            # Start test in background thread
            test_thread = threading.Thread(target=self.load_tester.run_test, daemon=True)
            test_thread.start()
            
            self.is_running = True
            self.control_button.text = "STOP TEST"
            self.control_button.md_bg_color = (1, 0, 0, 1)
            
            # Schedule stats updates
            self.stats_update_event = Clock.schedule_interval(self.refresh_stats, 1)
            
            # Save configuration
            self.save_config()
            
        except ValueError:
            self.show_dialog("Error", "Please enter valid numbers")
    
    def stop_test(self):
        if self.load_tester:
            self.load_tester.stop()
        
        self.is_running = False
        self.control_button.text = "START TEST"
        self.control_button.md_bg_color = self.control_button.theme_cls.primary_color
        
        if self.stats_update_event:
            self.stats_update_event.cancel()
    
    def update_stats(self, stats):
        """Called from background thread"""
        Clock.schedule_once(lambda dt: self._update_stats_ui(stats), 0)
    
    def _update_stats_ui(self, stats):
        """Update UI on main thread"""
        text = f"""[b]Test Statistics[/b]

[color=00ff00]✓ Successful:[/color] {stats['successful']:,}
[color=ff0000]✗ Failed:[/color] {stats['failed']:,}
[color=ffff00]🛡 WAF Blocks:[/color] {stats['waf_blocks']:,}
[color=ff8800]⏳ Rate Limits:[/color] {stats['rate_limits']:,}
[color=ff0000]⚠ Server Errors:[/color] {stats['server_errors']:,}

[b]Progress:[/b] {stats['progress']:.1f}%
[b]Success Rate:[/b] {stats['success_rate']:.1f}%
[b]RPS:[/b] {stats['rps']:.1f}

[b]Response Times:[/b]
  Avg: {stats['avg_response']:.3f}s
  Min: {stats['min_response']:.3f}s
  Max: {stats['max_response']:.3f}s

[b]Data Received:[/b] {stats['bytes_received'] / 1024 / 1024:.2f} MB

[b]Status:[/b] {stats['status']}
"""
        self.stats_label.text = text
        
        # Save stats to file
        self.save_stats(stats)
    
    def refresh_stats(self, dt):
        """Periodic refresh"""
        if self.load_tester:
            stats = self.load_tester.get_stats()
            self._update_stats_ui(stats)
    
    def save_config(self):
        """Save configuration"""
        config = {
            'url': self.url_input.text,
            'requests': self.requests_input.text,
            'threads': self.threads_input.text
        }
        
        try:
            with open(self.get_data_path('config.json'), 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def load_saved_data(self):
        """Load saved configuration"""
        try:
            config_path = self.get_data_path('config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.url_input.text = config.get('url', '')
                    self.requests_input.text = config.get('requests', '1000')
                    self.threads_input.text = config.get('threads', '50')
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def save_stats(self, stats):
        """Save statistics to file"""
        try:
            stats_file = self.get_data_path('stats_history.json')
            
            # Load existing stats
            history = []
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    history = json.load(f)
            
            # Add current stats with timestamp
            stats['timestamp'] = datetime.now().isoformat()
            history.append(stats)
            
            # Keep only last 100 entries
            history = history[-100:]
            
            # Save
            with open(stats_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Error saving stats: {e}")
    
    def get_data_path(self, filename):
        """Get platform-specific data path"""
        if platform == 'android':
            from android.storage import app_storage_path
            data_dir = app_storage_path()
        else:
            data_dir = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(data_dir, filename)
    
    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()


class LoadTesterApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return MainScreen()
    
    def on_start(self):
        """Request permissions on Android"""
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.INTERNET,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WAKE_LOCK,
                Permission.FOREGROUND_SERVICE
            ])
    
    def on_pause(self):
        """Allow app to run in background"""
        return True
    
    def on_resume(self):
        """Resume from background"""
        pass


if __name__ == '__main__':
    LoadTesterApp().run()
