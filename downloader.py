import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, url):
        QThread.__init__(self)
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            downloaded = 0

            with open(self.url.split('/')[-1], 'wb') as file:
                for data in response.iter_content(block_size):
                    size = file.write(data)
                    downloaded += size
                    if total_size > 0:
                        self.progress.emit(int(downloaded * 100 / total_size))

            self.finished.emit("Download completed successfully")
        except Exception as e:
            self.finished.emit(f"Error during download: {str(e)}")

class Downloader(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Enter package URL to download:"))
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)
        
        self.download_button = QPushButton("Download Package")
        self.download_button.clicked.connect(self.download_package)
        layout.addWidget(self.download_button)
        
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)
        
        self.setLayout(layout)

    def download_package(self):
        url = self.url_input.text()
        if url:
            self.download_button.setEnabled(False)
            self.progress_bar.setValue(0)
            self.status_text.clear()
            self.main_window.update_status(f"Downloading package from: {url}")
            
            self.thread = DownloadThread(url)
            self.thread.progress.connect(self.update_progress)
            self.thread.finished.connect(self.download_finished)
            self.thread.start()
        else:
            self.main_window.update_status("Please enter a package URL")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def download_finished(self, message):
        self.status_text.append(message)
        self.main_window.update_status(message)
        self.download_button.setEnabled(True)
