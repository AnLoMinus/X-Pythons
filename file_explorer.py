import os
import subprocess
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTreeView, QPushButton, QFileSystemModel, QHBoxLayout, QTextEdit
from PyQt5.QtCore import QDir, Qt

class FileExplorer(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.currentPath()))
        self.tree.setColumnWidth(0, 250)
        
        layout.addWidget(QLabel("File Explorer:"))
        layout.addWidget(self.tree)
        
        button_layout = QHBoxLayout()
        run_button = QPushButton("Run Selected Script")
        run_button.clicked.connect(self.run_script)
        button_layout.addWidget(run_button)
        
        edit_button = QPushButton("Edit Selected File")
        edit_button.clicked.connect(self.edit_file)
        button_layout.addWidget(edit_button)
        
        layout.addLayout(button_layout)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(QLabel("Output:"))
        layout.addWidget(self.output)
        
        self.setLayout(layout)

    def run_script(self):
        selected = self.tree.selectedIndexes()
        if selected:
            file_path = self.model.filePath(selected[0])
            if file_path.endswith('.py'):
                self.main_window.update_status(f"Running script: {file_path}")
                try:
                    result = subprocess.run(['python', file_path], capture_output=True, text=True)
                    self.output.setPlainText(result.stdout + result.stderr)
                except Exception as e:
                    self.output.setPlainText(f"Error running script: {str(e)}")
            else:
                self.main_window.update_status("Selected file is not a Python script")
        else:
            self.main_window.update_status("No file selected")

    def edit_file(self):
        selected = self.tree.selectedIndexes()
        if selected:
            file_path = self.model.filePath(selected[0])
            if os.path.isfile(file_path):
                self.main_window.open_file_in_editor(file_path)
            else:
                self.main_window.update_status("Selected item is not a file")
        else:
            self.main_window.update_status("No file selected")
