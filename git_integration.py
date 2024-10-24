from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QInputDialog
import subprocess

class GitIntegration(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        init_button = QPushButton("Initialize Git Repository")
        init_button.clicked.connect(self.init_repo)
        layout.addWidget(init_button)

        commit_button = QPushButton("Commit Changes")
        commit_button.clicked.connect(self.commit_changes)
        layout.addWidget(commit_button)

        push_button = QPushButton("Push Changes")
        push_button.clicked.connect(self.push_changes)
        layout.addWidget(push_button)

        self.setLayout(layout)

    def init_repo(self):
        try:
            result = subprocess.run(['git', 'init'], capture_output=True, text=True)
            self.output.setPlainText(result.stdout + result.stderr)
        except Exception as e:
            self.output.setPlainText(f"Error: {str(e)}")

    def commit_changes(self):
        message, ok = QInputDialog.getText(self, "Commit Message", "Enter commit message:")
        if ok and message:
            try:
                subprocess.run(['git', 'add', '.'], check=True)
                result = subprocess.run(['git', 'commit', '-m', message], capture_output=True, text=True)
                self.output.setPlainText(result.stdout + result.stderr)
            except Exception as e:
                self.output.setPlainText(f"Error: {str(e)}")

    def push_changes(self):
        try:
            result = subprocess.run(['git', 'push'], capture_output=True, text=True)
            self.output.setPlainText(result.stdout + result.stderr)
        except Exception as e:
            self.output.setPlainText(f"Error: {str(e)}")
