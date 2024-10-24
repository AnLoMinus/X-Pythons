from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
import unittest
import io
import sys

class UnitTester(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        test_button = QPushButton("Run Tests")
        test_button.clicked.connect(self.run_tests)
        layout.addWidget(test_button)

        self.setLayout(layout)

    def run_tests(self):
        code = self.main_window.code_editor.editor.toPlainText()
        
        # Redirect stdout to capture test results
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            # Create a test suite and run the tests
            suite = unittest.TestLoader().loadTestsFromModule(unittest.defaultTestLoader.loadTestsFromModule(unittest.mock.MagicMock()))
            unittest.TextTestRunner(stream=captured_output).run(suite)
        except Exception as e:
            print(f"Error running tests: {str(e)}")
        finally:
            # Restore stdout
            sys.stdout = sys.__stdout__

        self.output.setPlainText(captured_output.getvalue())
