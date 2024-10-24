import subprocess
import requests
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, 
                             QHBoxLayout, QTabWidget, QCheckBox, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
import os

class PyPISearchThread(QThread):
    result_ready = pyqtSignal(list)

    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        try:
            url = f"https://pypi.org/pypi/{self.query}/json"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.result_ready.emit([data['info']['name']])
            else:
                url = "https://pypi.org/simple/"
                response = requests.get(url)
                packages = [pkg for pkg in response.text.split('\n') if self.query.lower() in pkg.lower()]
                self.result_ready.emit(packages[:100])  # Limit to 100 results
        except Exception as e:
            self.result_ready.emit([f"Error: {str(e)}"])

class Installer(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.search_thread = None
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
        layout = QVBoxLayout()
        
        # Search field for available packages
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search available packages...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        search_layout.addWidget(self.search_input)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.load_available_packages)
        search_layout.addWidget(refresh_button)
        
        layout.addLayout(search_layout)
        
        # Create tabs for categories
        self.category_tabs = QTabWidget()
        categories = {
            "Web Development": ["Django", "Flask", "FastAPI", "Pyramid", "Tornado", "Bottle", "Dash", "Falcon", "Hug", "Sanic",
                                "Quart", "Starlette", "Responder", "Masonite", "BlackSheep", "Aiohttp", "CherryPy", "Web2py",
                                "TurboGears", "Morepath", "Growler", "Bocadillo", "Molten", "Japronto"],
            "Data Science": ["NumPy", "Pandas", "Matplotlib", "Scikit-learn", "SciPy", "Seaborn", "Plotly", "Statsmodels", "NLTK", "Gensim",
                             "TensorFlow", "PyTorch", "Keras", "XGBoost", "LightGBM", "Theano", "Caffe", "MXNet", "Chainer", "PyMC3",
                             "SymPy", "Bokeh", "Altair", "Dash"],
            "Machine Learning": ["TensorFlow", "PyTorch", "Keras", "XGBoost", "LightGBM", "Scikit-learn", "Theano", "Caffe", "MXNet", "Chainer",
                                 "CatBoost", "H2O", "Shogun", "Orange3", "PyCaret", "TPOT", "Auto-sklearn", "MLflow", "Optuna", "Ray",
                                 "Dask-ML", "PyBrain", "Lasagne", "Gluon"],
            "Utilities": ["Requests", "Beautiful Soup", "Pillow", "PyYAML", "Pytest", "Celery", "SQLAlchemy", "Scrapy", "Paramiko", "Fabric",
                          "Click", "Loguru", "Pydantic", "Tqdm", "Arrow", "Dateutil", "Tabulate", "Rich", "Colorama", "Faker",
                          "Jinja2", "MarkupSafe", "Werkzeug", "WTForms"],
            "Networking": ["Twisted", "asyncio", "socket", "paramiko", "pyzmq", "requests", "httpx", "aiohttp", "websockets", "pycurl",
                           "Scapy", "Pyshark", "Netmiko", "Napalm", "Nornir", "PySNMP", "PyModbus", "PyZMQ", "PySerial", "PyBluez",
                           "PyRFC", "PyCURL", "PySocks", "PyNMAP"],
            "Database": ["SQLAlchemy", "Psycopg2", "PyMySQL", "SQLite", "MongoDB", "PyMongo", "Redis", "Cassandra", "Elasticsearch", "InfluxDB",
                         "SQLObject", "Peewee", "Tortoise-ORM", "Django ORM", "Pony ORM", "Orator", "Gino", "Databases", "TinyDB", "ZODB",
                         "PickleDB", "UnQLite", "Firebird", "RethinkDB"],
            "Testing": ["Pytest", "Unittest", "Nose", "Hypothesis", "tox", "coverage", "mock", "pytest-cov", "pytest-mock", "pytest-asyncio",
                        "Robot Framework", "Behave", "Lettuce", "Testify", "TestProject", "Testinfra", "Testcontainers", "PyHamcrest", "PyVows", "PyUnit",
                        "PyUnitReport", "PyUnitTest", "PyUnitTestRunner", "PyUnitTestSuite"],
            "Security": ["Cryptography", "PyCrypto", "PyOpenSSL", "paramiko", "bcrypt", "hashlib", "ssl", "pycryptodome", "passlib", "jwt",
                         "PyNaCl", "PyCryptodome", "PyCryptoDomeX", "PyCryptoPlus", "PyCryptoJS", "PyCryptoRSA", "PyCryptoAES", "PyCryptoDES", "PyCryptoBlowfish", "PyCryptoTwofish",
                         "PyCryptoSerpent", "PyCryptoCamellia", "PyCryptoCAST", "PyCryptoIDEA", "PyCryptoRC2", "PyCryptoRC4", "PyCryptoRC5"],
            "System": ["psutil", "pywin32", "watchdog", "python-daemon", "schedule", "APScheduler", "supervisor", "pyinstaller", "cx_Freeze", "py2exe",
                       "pyautogui", "pynput", "pywinauto", "pygetwindow", "pyperclip", "winshell", "pyuac", "pywin32-ctypes", "wmi", "pyreadline",
                       "pyserial", "pyusb", "pyi2c", "pyspi", "pyserial-asyncio", "pyftdi"],
            "Audio": ["pydub", "pyaudio", "sounddevice", "librosa", "pygame", "simpleaudio", "playsound", "pysoundfile", "audioread", "mutagen",
                      "pydub", "tinytag", "pySoundCard", "pyalsaaudio", "soundfile", "python-sounddevice", "pyo", "pyaudioanalysis", "aubio", "madmom",
                      "pyAudioAnalysis", "essentia", "mido", "pretty_midi", "music21"]
        }
        
        for category, libraries in categories.items():
            tab = QWidget()
            tab_layout = QVBoxLayout()
            scroll_area = QScrollArea()
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout()
            
            for library in libraries:
                checkbox = QCheckBox(library)
                scroll_layout.addWidget(checkbox)
            
            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)
            scroll_area.setWidgetResizable(True)
            tab_layout.addWidget(scroll_area)
            tab.setLayout(tab_layout)
            self.category_tabs.addTab(tab, category)
        
        layout.addWidget(self.category_tabs)
        
        install_button = QPushButton("Install Selected Packages")
        install_button.clicked.connect(self.install_selected_packages)
        layout.addWidget(install_button)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(QLabel("Installation Output:"))
        layout.addWidget(self.output)
        
        self.setLayout(layout)

    def load_available_packages(self):
        self.main_window.update_status("Categories and popular packages loaded")

    def on_search_text_changed(self):
        self.search_timer.stop()
        self.search_timer.start(300)  # Wait for 300ms before performing the search

    def perform_search(self):
        query = self.search_input.text()
        if self.search_thread is not None and self.search_thread.isRunning():
            self.search_thread.terminate()
            self.search_thread.wait()
        self.search_thread = PyPISearchThread(query)
        self.search_thread.result_ready.connect(self.update_search_results)
        self.search_thread.start()

    def update_search_results(self, packages):
        self.output.clear()
        self.output.append("Search Results:")
        for package in packages:
            self.output.append(package)
        self.main_window.update_status(f"Found {len(packages)} packages matching your search")

    def install_selected_packages(self):
        selected_packages = []
        for i in range(self.category_tabs.count()):
            tab = self.category_tabs.widget(i)
            scroll_area = tab.findChild(QScrollArea)
            scroll_widget = scroll_area.widget()
            for checkbox in scroll_widget.findChildren(QCheckBox):
                if checkbox.isChecked():
                    selected_packages.append(checkbox.text())
        
        if selected_packages:
            self.output.clear()
            self.output.append(f"Installing packages: {', '.join(selected_packages)}")
            self.main_window.update_status(f"Installing {len(selected_packages)} packages...")
            
            # Get the path to the active virtual environment
            active_venv_path = self.main_window.virtual_env_manager.get_active_venv_path()

            if active_venv_path:
                for package in selected_packages:
                    try:
                        # Use the pip executable from the active virtual environment
                        pip_executable = os.path.join(active_venv_path, 'bin', 'pip')
                        result = subprocess.run([pip_executable, 'install', package], capture_output=True, text=True)
                        self.output.append(f"\nInstalling {package}:\n{result.stdout}\n{result.stderr}")
                        if result.returncode == 0:
                            self.main_window.update_status(f"Successfully installed {package}")
                        else:
                            self.main_window.update_status(f"Failed to install {package}")
                    except Exception as e:
                        self.output.append(f"\nError installing {package}: {str(e)}")
                        self.main_window.update_status(f"Error installing {package}")
            else:
                self.main_window.update_status("No active virtual environment. Please activate one before installing packages.")
        else:
            self.main_window.update_status("No packages selected for installation")

    def closeEvent(self, event):
        if self.search_thread is not None and self.search_thread.isRunning():
            self.search_thread.terminate()
            self.search_thread.wait()
        super().closeEvent(event)
