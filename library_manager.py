import pkg_resources
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QInputDialog, QLineEdit, QComboBox
from PyQt5.QtCore import Qt, QTimer
import subprocess
import os

class LibraryManager(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        
        # Add view selector
        self.view_selector = QComboBox()
        self.view_selector.addItems(["System Libraries", "Virtual Environment Libraries"])
        self.view_selector.currentIndexChanged.connect(self.refresh_libraries)
        layout.addWidget(self.view_selector)
        
        # Add search field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search libraries...")
        self.search_input.textChanged.connect(self.filter_libraries)
        layout.addWidget(self.search_input)
        
        self.library_list = QListWidget()
        layout.addWidget(QLabel("Installed Libraries:"))
        layout.addWidget(self.library_list)
        
        button_layout = QHBoxLayout()
        refresh_button = QPushButton("Refresh Library List")
        refresh_button.clicked.connect(self.refresh_libraries)
        button_layout.addWidget(refresh_button)
        
        update_button = QPushButton("Update Selected")
        update_button.clicked.connect(self.update_library)
        button_layout.addWidget(update_button)
        
        remove_button = QPushButton("Remove Selected")
        remove_button.clicked.connect(self.remove_library)
        button_layout.addWidget(remove_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        self.all_packages = []
        self.refresh_libraries()

    def refresh_libraries(self):
        self.library_list.clear()
        self.all_packages = []
        
        if self.view_selector.currentText() == "System Libraries":
            self.all_packages = [f"{d.project_name}=={d.version}" for d in pkg_resources.working_set]
        else:
            active_venv_path = self.main_window.virtual_env_manager.get_active_venv_path()
            if active_venv_path:
                pip_executable = os.path.join(active_venv_path, 'bin', 'pip')
                result = subprocess.run([pip_executable, 'list', '--format=freeze'], capture_output=True, text=True)
                self.all_packages = result.stdout.splitlines()
            else:
                self.all_packages = ["No active virtual environment"]
        
        self.library_list.addItems(self.all_packages)
        self.main_window.update_status("Library list refreshed")

    def filter_libraries(self):
        search_text = self.search_input.text().lower()
        self.library_list.clear()
        for package in self.all_packages:
            if search_text in package.lower():
                self.library_list.addItem(package)

    def update_library(self):
        selected = self.library_list.currentItem()
        if selected:
            library = selected.text().split('==')[0]
            self.main_window.update_status(f"Updating {library}...")
            
            if self.view_selector.currentText() == "Virtual Environment Libraries":
                active_venv_path = self.main_window.virtual_env_manager.get_active_venv_path()
                if active_venv_path:
                    pip_executable = os.path.join(active_venv_path, 'bin', 'pip')
                    result = subprocess.run([pip_executable, 'install', '--upgrade', library], capture_output=True, text=True)
                    if result.returncode == 0:
                        self.main_window.update_status(f"{library} updated successfully in virtual environment")
                    else:
                        self.main_window.update_status(f"Failed to update {library} in virtual environment")
                else:
                    self.main_window.update_status("No active virtual environment")
            else:
                # Update system-wide package (requires appropriate permissions)
                result = subprocess.run(['pip', 'install', '--upgrade', library], capture_output=True, text=True)
                if result.returncode == 0:
                    self.main_window.update_status(f"{library} updated successfully")
                else:
                    self.main_window.update_status(f"Failed to update {library}")
            
            self.refresh_libraries()
        else:
            self.main_window.update_status("No library selected")

    def remove_library(self):
        selected = self.library_list.currentItem()
        if selected:
            library = selected.text().split('==')[0]
            confirm, _ = QInputDialog.getText(self, 'Confirm Removal', 
                                              f"Type 'yes' to confirm removal of {library}:")
            if confirm.lower() == 'yes':
                self.main_window.update_status(f"Removing {library}...")
                
                if self.view_selector.currentText() == "Virtual Environment Libraries":
                    active_venv_path = self.main_window.virtual_env_manager.get_active_venv_path()
                    if active_venv_path:
                        pip_executable = os.path.join(active_venv_path, 'bin', 'pip')
                        result = subprocess.run([pip_executable, 'uninstall', '-y', library], capture_output=True, text=True)
                        if result.returncode == 0:
                            self.main_window.update_status(f"{library} removed successfully from virtual environment")
                        else:
                            self.main_window.update_status(f"Failed to remove {library} from virtual environment")
                    else:
                        self.main_window.update_status("No active virtual environment")
                else:
                    # Remove system-wide package (requires appropriate permissions)
                    result = subprocess.run(['pip', 'uninstall', '-y', library], capture_output=True, text=True)
                    if result.returncode == 0:
                        self.main_window.update_status(f"{library} removed successfully")
                    else:
                        self.main_window.update_status(f"Failed to remove {library}")
                
                self.refresh_libraries()
            else:
                self.main_window.update_status("Removal cancelled")
        else:
            self.main_window.update_status("No library selected")
