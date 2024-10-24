from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeView, QPushButton, QFileSystemModel, QInputDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import QDir

class ProjectManager(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_project_path = QDir.currentPath()  # Set default path
        layout = QVBoxLayout()

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.current_project_path))
        self.tree.setColumnWidth(0, 250)

        layout.addWidget(self.tree)

        new_project_button = QPushButton("New Project")
        new_project_button.clicked.connect(self.create_new_project)
        layout.addWidget(new_project_button)

        open_project_button = QPushButton("Open Project")
        open_project_button.clicked.connect(self.open_project)
        layout.addWidget(open_project_button)

        self.setLayout(layout)

    def create_new_project(self):
        project_name, ok = QInputDialog.getText(self, "New Project", "Enter project name:")
        if ok and project_name:
            project_path = QDir.currentPath() + "/" + project_name
            if QDir().mkpath(project_path):
                self.current_project_path = project_path
                self.tree.setRootIndex(self.model.index(self.current_project_path))
                self.main_window.update_current_project_path(project_path)
            else:
                QMessageBox.warning(self, "Error", "Failed to create project directory")

    def get_current_project_path(self):
        return self.current_project_path

    def open_project(self):
        project_path = QFileDialog.getExistingDirectory(self, "Open Project")
        if project_path:
            self.current_project_path = project_path
            self.tree.setRootIndex(self.model.index(self.current_project_path))
            self.main_window.update_current_project_path(project_path)
