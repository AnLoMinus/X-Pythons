from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QInputDialog
import subprocess
import venv
import os

class VirtualEnvManager(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        create_button = QPushButton("Create Virtual Environment")
        create_button.clicked.connect(self.create_venv)
        layout.addWidget(create_button)

        activate_button = QPushButton("Activate Virtual Environment")
        activate_button.clicked.connect(self.activate_venv)
        layout.addWidget(activate_button)

        list_venvs_button = QPushButton("List Virtual Environments")
        list_venvs_button.clicked.connect(self.list_venvs)
        layout.addWidget(list_venvs_button)

        self.setLayout(layout)

        # Ensure the directory for virtual environments exists
        self.venv_dir = os.path.join(os.getcwd(), 'Virtuals-Environment')
        os.makedirs(self.venv_dir, exist_ok=True)
        self.active_venv_path = None

    def create_venv(self):
        venv_name, ok = QInputDialog.getText(self, "Create Virtual Environment", "Enter venv name:")
        if ok and venv_name:
            venv_path = os.path.join(self.venv_dir, venv_name)
            try:
                venv.create(venv_path, with_pip=True)
                self.output.setPlainText(f"Virtual environment '{venv_name}' created successfully in {self.venv_dir}.")
            except Exception as e:
                self.output.setPlainText(f"Error creating virtual environment: {str(e)}")

    def activate_venv(self):
        venv_name, ok = QInputDialog.getText(self, "Activate Virtual Environment", "Enter venv name:")
        if ok and venv_name:
            activate_script = os.path.join(self.venv_dir, venv_name, 'bin', 'activate')
            if os.path.exists(activate_script):
                self.active_venv_path = os.path.join(self.venv_dir, venv_name)
                self.output.setPlainText(f"Virtual environment '{venv_name}' activated.")
            else:
                self.output.setPlainText(f"Virtual environment '{venv_name}' not found.")

    def list_venvs(self):
        if os.path.exists(self.venv_dir):
            venvs = [d for d in os.listdir(self.venv_dir) if os.path.isdir(os.path.join(self.venv_dir, d))]
            self.output.setPlainText("Available virtual environments:\n" + "\n".join(venvs))
        else:
            self.output.setPlainText("No virtual environments found.")

    def get_active_venv_path(self):
        return self.active_venv_path
