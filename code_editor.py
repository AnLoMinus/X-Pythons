from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QPushButton, QHBoxLayout, QCompleter
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QSyntaxHighlighter
from PyQt5.QtCore import QRegExp, Qt
import keyword
from PyQt5.QtCore import QStringListModel

class MultiLanguageHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.language = "Python"
        self.highlightingRules = {}
        self.init_python_rules()
        self.init_javascript_rules()

    def init_python_rules(self):
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Bold)

        keywords = keyword.kwlist

        self.highlightingRules["Python"] = [(QRegExp(r'\b' + word + r'\b'), keyword_format) for word in keywords]

    def init_javascript_rules(self):
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Bold)

        keywords = ["var", "let", "const", "function", "if", "else", "for", "while", "return", "class", "import", "export"]

        self.highlightingRules["JavaScript"] = [(QRegExp(r'\b' + word + r'\b'), keyword_format) for word in keywords]

    def set_language(self, language):
        self.language = language
        self.rehighlight()

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules.get(self.language, []):
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

class CodeEditor(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.file_path = None
        layout = QVBoxLayout()

        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("Courier New", 12))  # Changed to a more common monospace font
        self.highlighter = MultiLanguageHighlighter(self.editor.document())
        layout.addWidget(self.editor)

        # Add auto-completion
        self.completer = QCompleter(keyword.kwlist)
        self.completer.setWidget(self.editor)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.editor.textChanged.connect(self.show_autocomplete)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_file)
        button_layout.addWidget(save_button)

        run_button = QPushButton("Run")
        run_button.clicked.connect(self.run_code)
        button_layout.addWidget(run_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def set_language(self, language):
        self.highlighter.set_language(language)
        if language == "JavaScript":
            self.completer.setModel(QStringListModel(["var", "let", "const", "function", "if", "else", "for", "while", "return", "class", "import", "export"]))
        else:  # Default to Python
            self.completer.setModel(QStringListModel(keyword.kwlist))

    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, 'w') as file:
                    file.write(self.editor.toPlainText())
                self.main_window.update_status(f"File saved: {self.file_path}")
            except Exception as e:
                self.main_window.update_status(f"Error saving file: {str(e)}")
        else:
            self.main_window.update_status("No file path set. Use 'Save As' instead.")

    def run_code(self):
        # Implement code execution
        self.main_window.update_status("Code executed")

    def show_autocomplete(self):
        tc = self.editor.textCursor()
        tc.select(tc.WordUnderCursor)
        cr = self.editor.cursorRect()

        if len(tc.selectedText()) > 0:
            self.completer.setCompletionPrefix(tc.selectedText())
            popup = self.completer.popup()
            popup.setCurrentIndex(self.completer.completionModel().index(0,0))

            cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cr)
        else:
            self.completer.popup().hide()

    def load_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.editor.setPlainText(content)
            self.file_path = file_path
            self.main_window.update_status(f"Loaded file: {file_path}")
        except Exception as e:
            self.main_window.update_status(f"Error loading file: {str(e)}")
