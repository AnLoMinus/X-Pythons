from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
import pdb
import sys
import io

class DebuggerThread(QThread):
    output_ready = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, code):
        super().__init__()
        self.code = code

    def run(self):
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        try:
            debugger = pdb.Pdb(stdout=redirected_output)
            debugger.run(self.code)
        except Exception as e:
            print(f"Error during debugging: {str(e)}")
        finally:
            sys.stdout = old_stdout
            output = redirected_output.getvalue()
            self.output_ready.emit(output)
            self.finished.emit()

class Debugger(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        debug_button = QPushButton("Start Debugging")
        debug_button.clicked.connect(self.start_debugging)
        layout.addWidget(debug_button)

        self.setLayout(layout)

    def start_debugging(self):
        code = self.main_window.code_editor.editor.toPlainText()
        self.output.clear()
        self.output.setPlainText("Starting debugging session...")
        
        self.debug_thread = DebuggerThread(code)
        self.debug_thread.output_ready.connect(self.update_output)
        self.debug_thread.finished.connect(self.debugging_finished)
        self.debug_thread.start()

    def update_output(self, text):
        self.output.append(text)

    def debugging_finished(self):
        self.output.append("Debugging session ended.")
        self.main_window.update_status("Debugging session ended")
