import subprocess
import os

class IDEIntegration:
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_project_path = None

    def update_project_path(self, path):
        self.current_project_path = path

    def open_in_vscode(self):
        if self.current_project_path:
            try:
                subprocess.Popen(["code", self.current_project_path])
                self.main_window.update_status(f"Opened project in VS Code: {self.current_project_path}")
            except FileNotFoundError:
                self.main_window.update_status("VS Code not found. Please make sure it's installed and in your PATH.")
        else:
            self.main_window.update_status("No project is currently open.")

    def open_in_pycharm(self):
        if self.current_project_path:
            try:
                subprocess.Popen(["pycharm", self.current_project_path])
                self.main_window.update_status(f"Opened project in PyCharm: {self.current_project_path}")
            except FileNotFoundError:
                self.main_window.update_status("PyCharm not found. Please make sure it's installed and in your PATH.")
        else:
            self.main_window.update_status("No project is currently open.")
