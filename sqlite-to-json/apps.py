import sys
import sqlite3
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit


class SQLiteToJsonConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SQLite to JSON Converter')
        self.setGeometry(100, 100, 400, 300)

        self.btnOpenFile = QPushButton('Open SQLite File', self)
        self.btnOpenFile.clicked.connect(self.openFile)

        self.textOutput = QTextEdit(self)
        self.textOutput.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.btnOpenFile)
        layout.addWidget(self.textOutput)

        self.setLayout(layout)

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open SQLite File", "", "SQLite Files (*.sqlite *.db);;All Files (*)", options=options)
        if fileName:
            json_data = self.convert_sqlite_to_json(fileName)
            self.textOutput.setPlainText(json_data)

    def convert_sqlite_to_json(self, sqlite_file):
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        data = {}

        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            table_data = []
            for row in rows:
                row_dict = {}
                for i, column in enumerate(cursor.description):
                    row_dict[column[0]] = row[i]
                table_data.append(row_dict)

            data[table_name] = table_data

        conn.close()

        return json.dumps(data, indent=4)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SQLiteToJsonConverter()
    ex.show()
    sys.exit(app.exec_())
