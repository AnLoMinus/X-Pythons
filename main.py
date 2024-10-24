import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QTabWidget, QFileDialog, QMenuBar, QAction,
                             QMessageBox, QDialog, QVBoxLayout, QTextEdit, QInputDialog, QLineEdit,
                             QDockWidget, QComboBox, QHBoxLayout)
from PyQt5.QtCore import Qt, QSettings, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from library_manager import LibraryManager
from file_explorer import FileExplorer
from downloader import Downloader
from installer import Installer
from code_editor import CodeEditor
from project_manager import ProjectManager
from git_integration import GitIntegration
from debugger import Debugger
from unit_tester import UnitTester
from virtual_env_manager import VirtualEnvManager
from terminal import Terminal
from collaboration_manager import CollaborationManager
from ai_assistant import AIAssistant
from ide_integration import IDEIntegration
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('X-Pythons v0.9.0 - Developed by AnLoMinus')  # Updated title
        self.setGeometry(100, 100, 1400, 1000)

        # Setup logging
        logging.basicConfig(filename='x_pythons.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Load settings
        self.settings = QSettings('X-Pythons', 'v0.9.0')
        self.load_settings()

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create and add header label
        header_label = QLabel('Welcome to X-Pythons v0.9.0 - Developed by AnLoMinus')  # Updated header
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Initialize tabs
        self.init_tabs()

        # Initialize IDE integration
        self.ide_integration = IDEIntegration(self)

        # Create menu bar
        self.create_menu_bar()

        # Initialize collaboration manager
        self.collaboration_manager = CollaborationManager(self)

        # Initialize AI assistant
        self.ai_assistant = AIAssistant(self)

        # Status Bar
        self.statusBar().showMessage('Ready')

        # Performance optimization: Lazy loading of modules
        self.lazy_load_modules()

        # Create dock widgets after lazy loading
        self.create_dock_widgets()

        # Set focus to the main window to ensure menu bar is accessible
        self.activateWindow()
        self.raise_()
        self.setFocus()

        logging.info('Application started')

    def init_tabs(self):
        self.library_manager = LibraryManager(self)
        self.tab_widget.addTab(self.library_manager, "📚 Library Manager")

        self.file_explorer = FileExplorer(self)
        self.tab_widget.addTab(self.file_explorer, "🗂 File Explorer")

        self.downloader = Downloader(self)
        self.tab_widget.addTab(self.downloader, "⬇️ Downloader")

        self.installer = Installer(self)
        self.tab_widget.addTab(self.installer, "📦 Installer")

        self.code_editor = CodeEditor(self)
        self.tab_widget.addTab(self.code_editor, "📝 Code Editor")

        self.project_manager = ProjectManager(self)
        self.tab_widget.addTab(self.project_manager, "🏗 Project Manager")

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        settings_menu = menu_bar.addMenu('Settings')
        theme_action = QAction('Change Theme', self)
        theme_action.triggered.connect(self.change_theme)
        settings_menu.addAction(theme_action)

        language_action = QAction('Change Language', self)
        language_action.triggered.connect(self.change_language)
        settings_menu.addAction(language_action)

        help_menu = menu_bar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        docs_action = QAction('Documentation', self)
        docs_action.triggered.connect(self.show_documentation)
        help_menu.addAction(docs_action)

        ide_menu = self.menuBar().addMenu('IDE Integration')
        vscode_action = QAction('Open in VS Code', self)
        vscode_action.triggered.connect(self.ide_integration.open_in_vscode)
        ide_menu.addAction(vscode_action)

        pycharm_action = QAction('Open in PyCharm', self)
        pycharm_action.triggered.connect(self.ide_integration.open_in_pycharm)
        ide_menu.addAction(pycharm_action)

        # הוספת פעולה חדשה לתפריט העזרה
        about_contributors_action = QAction('About Contributors', self)
        about_contributors_action.triggered.connect(self.show_about_contributors)
        help_menu.addAction(about_contributors_action)

    def create_dock_widgets(self):
        git_dock = QDockWidget("🔀 Git Integration", self)
        git_dock.setWidget(self.git_integration)
        self.addDockWidget(Qt.RightDockWidgetArea, git_dock)

        debug_dock = QDockWidget("🐞 Debugger", self)
        debug_dock.setWidget(self.debugger)
        self.addDockWidget(Qt.BottomDockWidgetArea, debug_dock)

        test_dock = QDockWidget("🧪 Unit Tester", self)
        test_dock.setWidget(self.unit_tester)
        self.addDockWidget(Qt.BottomDockWidgetArea, test_dock)

        venv_dock = QDockWidget("🐍 Virtual Environment", self)
        venv_dock.setWidget(self.virtual_env_manager)
        self.addDockWidget(Qt.LeftDockWidgetArea, venv_dock)

        terminal_dock = QDockWidget("💻 Terminal", self)
        terminal_dock.setWidget(self.terminal)
        self.addDockWidget(Qt.BottomDockWidgetArea, terminal_dock)

        collab_dock = QDockWidget("👥 Collaboration", self)
        collab_dock.setWidget(self.collaboration_manager.get_widget())
        self.addDockWidget(Qt.RightDockWidgetArea, collab_dock)

        ai_dock = QDockWidget("🤖 AI Assistant", self)
        ai_dock.setWidget(self.ai_assistant)
        self.addDockWidget(Qt.RightDockWidgetArea, ai_dock)

    def lazy_load_modules(self):
        self.git_integration = GitIntegration(self)
        self.debugger = Debugger(self)
        self.unit_tester = UnitTester(self)
        self.virtual_env_manager = VirtualEnvManager(self)
        self.terminal = Terminal(self)

    def change_theme(self):
        themes = ["Light", "Dark", "Blue", "Green"]
        theme, ok = QInputDialog.getItem(self, "Select Theme", 
                                         "Choose your preferred theme:", 
                                         themes, 0, False)
        if ok and theme:
            self.apply_theme(theme)

    def apply_theme(self, theme):
        if theme == "Light":
            self.setStyleSheet("")
        elif theme == "Dark":
            self.setStyleSheet("""
                QWidget { background-color: #2b2b2b; color: #ffffff; }
                QMenuBar { background-color: #1e1e1e; }
                QMenuBar::item:selected { background-color: #3a3a3a; }
                QMenu { background-color: #2b2b2b; }
                QMenu::item:selected { background-color: #3a3a3a; }
            """)
        elif theme == "Blue":
            self.setStyleSheet("""
                QWidget { background-color: #1e3d59; color: #f5f0e1; }
                QMenuBar { background-color: #162b40; }
                QMenuBar::item:selected { background-color: #274c77; }
                QMenu { background-color: #1e3d59; }
                QMenu::item:selected { background-color: #274c77; }
            """)
        elif theme == "Green":
            self.setStyleSheet("""
                QWidget { background-color: #2c5f2d; color: #f0f7ee; }
                QMenuBar { background-color: #1e4620; }
                QMenuBar::item:selected { background-color: #3a3a3b; }
                QMenu { background-color: #2c5f2d; }
                QMenu::item:selected { background-color: #3a3a3b; }
            """)
        self.settings.setValue('theme', theme)

    def change_language(self):
        languages = ["Python", "JavaScript", "Java", "C++", "Ruby", "Go", "Rust"]
        language, ok = QInputDialog.getItem(self, "Select Language", 
                                            "Choose your preferred programming language:", 
                                            languages, 0, False)
        if ok and language:
            self.settings.setValue('language', language)
            self.code_editor.set_language(language)
            QMessageBox.information(self, "Language Changed", 
                                    f"Language changed to {language}.")

    def show_about(self):
        QMessageBox.about(self, "About X-Pythons", 
                          "X-Pythons v0.9.0\n\nDeveloped by AnLoMinus\n\nA comprehensive Python development environment.")

    def show_documentation(self):
        doc_dialog = QDialog(self)
        doc_dialog.setWindowTitle("X-Pythons Documentation")
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(self.load_documentation())
        layout.addWidget(text_edit)
        doc_dialog.setLayout(layout)
        doc_dialog.resize(600, 400)
        doc_dialog.exec_()

    def load_documentation(self):
        # Load documentation from a file or generate it dynamically
        return """
        <h1 style="text-align: center;">X-Pythons Documentation 📚</h1>
        <p>Welcome to <strong>X-Pythons</strong>, your comprehensive Python development environment. Below are detailed instructions on how to use the various features of the application:</p>
        
        <h2>Getting Started 🚀</h2>
        <ol>
            <li><strong>Clone the Repository:</strong> <code>git clone https://github.com/AnLoMinus/X-Pythons</code></li>
            <li><strong>Install Requirements:</strong> <code>pip install -r requirements.txt</code></li>
            <li><strong>Run the Application:</strong> <code>python main.py</code></li>
        </ol>
        
        <h2>Features Overview ✨</h2>
        <ul>
            <li><strong>Library Management 📚:</strong> View and manage libraries for both system-wide and virtual environments.</li>
            <li><strong>File Explorer 🗂️:</strong> Browse and execute Python scripts directly from the file explorer.</li>
            <li><strong>Package Installer 📥:</strong> Search and install packages from PyPI with categorized library tabs.</li>
            <li><strong>Code Editor 📝:</strong> Enjoy syntax highlighting and auto-completion for multiple languages.</li>
            <li><strong>Project Management 🏗️:</strong> Create and manage projects with integration to popular IDEs.</li>
            <li><strong>Git Integration 🔀:</strong> Easily manage your Git repositories with commit and push features.</li>
            <li><strong>Debugger 🐞:</strong> Step through your code and inspect variables with ease.</li>
            <li><strong>Unit Testing 🧪:</strong> Run and manage unit tests for your projects.</li>
            <li><strong>Virtual Environment Management 🐍:</strong> Create, activate, and manage virtual environments.</li>
            <li><strong>Integrated Terminal 💻:</strong> Execute shell commands directly within the application.</li>
            <li><strong>Collaboration Tools 👥:</strong> Share and collaborate on code in real-time.</li>
            <li><strong>AI-powered Suggestions 🤖:</strong> Get AI-driven suggestions for code improvements.</li>
            <li><strong>Customizable Themes 🎨:</strong> Choose from multiple themes to suit your preference.</li>
        </ul>
        
        <h2>Using the Application 🛠️</h2>
        <p>Navigate through the tabs to access different features. Use the menu bar for additional settings and help options.</p>
        
        <h2>Support and Feedback 📧</h2>
        <p>If you encounter any issues or have feedback, please contact us at <a href="mailto:areweleon@gmail.com">areweleon@gmail.com</a>.</p>
        <p>GitHub: <a href="https://github.com/AnLoMinus/X-Pythons">https://github.com/AnLoMinus/X-Pythons</a></p>
        
        <p style="text-align: center;">Thank you for using X-Pythons! Developed by AnLoMinus. We hope you enjoy your coding experience. 😊</p>
        """

    def update_status(self, message):
        self.statusBar().showMessage(message)
        logging.info(message)

    def load_settings(self):
        theme = self.settings.value('theme', 'Light')
        self.apply_theme(theme)

    def closeEvent(self, event):
        self.settings.sync()
        logging.info('Application closed')
        event.accept()

    # Add this method to the MainWindow class
    def update_current_project_path(self, path):
        self.current_project_path = path
        self.ide_integration.update_project_path(path)
        self.update_status(f"Current project: {path}")

    def open_file_in_editor(self, file_path):
        # Check if the file is already open in a tab
        for i in range(self.tab_widget.count()):
            if isinstance(self.tab_widget.widget(i), CodeEditor) and self.tab_widget.widget(i).file_path == file_path:
                self.tab_widget.setCurrentIndex(i)
                return

        # If the file is not open, create a new CodeEditor tab
        editor = CodeEditor(self)
        editor.load_file(file_path)
        editor.file_path = file_path
        tab_name = os.path.basename(file_path)
        self.tab_widget.addTab(editor, tab_name)
        self.tab_widget.setCurrentWidget(editor)
        self.update_status(f"Opened file: {file_path}")

    def show_about_contributors(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About Contributors and Technologies")
        layout = QVBoxLayout()

        # הוספת לוגו או תמונה (אם יש)
        logo_label = QLabel()
        logo_pixmap = QPixmap("path/to/logo.png")  # החלף עם הנתיב האמיתי ללוגו
        logo_label.setPixmap(logo_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        # מידע על המפתחים והטכנולוגיות
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setHtml("""
        <h2>X-Pythons v0.9.0</h2>
        <p>A comprehensive Python development environment.</p>
        
        <h3>Contributors:</h3>
        <ul>
            <li><strong>AnLoMinus</strong> - Lead Developer</li>
            <li><strong>Claude</strong> - AI Assistant Developer</li>
        </ul>

        <h3>Technologies:</h3>
        <ul>
            <li>Python 3.x</li>
            <li>PyQt5</li>
            <li>Git</li>
            <li>venv (Virtual Environments)</li>
            <li>pip (Package Installer)</li>
            <li>PyPI (Python Package Index)</li>
        </ul>

        <p>GitHub: <a href="https://github.com/AnLoMinus/X-Pythons">https://github.com/AnLoMinus/X-Pythons</a></p>
        <p>For support or inquiries, please contact: <a href="mailto:areweleon@gmail.com">areweleon@gmail.com</a></p>
        """)
        layout.addWidget(info_text)

        about_dialog.setLayout(layout)
        about_dialog.resize(400, 500)
        about_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
