from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit
import subprocess

class Terminal(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.input = QLineEdit()
        self.input.returnPressed.connect(self.execute_command)
        layout.addWidget(self.input)

        self.setLayout(layout)

    def execute_command(self):
        command = self.input.text()
        self.input.clear()
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            self.output.append(f"$ {command}")
            self.output.append(result.stdout)
            if result.stderr:
                self.output.append(result.stderr)
        except Exception as e:
            self.output.append(f"Error executing command: {str(e)}")
