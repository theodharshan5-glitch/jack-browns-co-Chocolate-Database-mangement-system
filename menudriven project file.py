import sys
import mysql.connector as mysql

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QComboBox,
    QTableWidget, QTableWidgetItem,
    QHeaderView
)

from PyQt5.QtCore import Qt


class DynamicDBMS(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Jack Browns & Co. DBMS")
        self.setGeometry(150, 50, 1300, 750)

        title = QLabel("Dynamic Database Manager")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        self.table_select = QComboBox()

        self.table = QTableWidget()

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        btn_load = QPushButton("LOAD TABLE")
        btn_add = QPushButton("ADD ROW")
        btn_delete = QPushButton("DELETE ROW")
        btn_save = QPushButton("SAVE CHANGES")

        btn_load.clicked.connect(self.load_table)
        btn_add.clicked.connect(self.add_row)
        btn_delete.clicked.connect(self.delete_row)
        btn_save.clicked.connect(self.save_changes)

        top_layout = QHBoxLayout()

        top_layout.addWidget(self.table_select)
        top_layout.addWidget(btn_load)
        top_layout.addWidget(btn_add)
        top_layout.addWidget(btn_delete)
        top_layout.addWidget(btn_save)

        main_layout = QVBoxLayout()

        main_layout.addWidget(title)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
  
        self.load_table_names()

        self.setStyleSheet("""

            QWidget {
                background-color: #121212;
                color: white;
                font-family: Segoe UI;
                font-size: 14px;
            }

            #title {
                font-size: 28px;
                font-weight: bold;
                color: cyan;
                padding: 10px;
            }

            QComboBox {
                background-color: #1f1f1f;
                border: 2px solid cyan;
                border-radius: 10px;
                padding: 10px;
                min-width: 200px;
            }

            QPushButton {
                background-color: #1e1e1e;
                border: 2px solid cyan;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: cyan;
                color: black;
            }

            QTableWidget {
                background-color: #1a1a1a;
                border: 2px solid cyan;
                border-radius: 10px;
                gridline-color: #333;
            }

            QHeaderView::section {
                background-color: cyan;
                color: black;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

    def connect_db(self):

        return mysql.connect(
            host='localhost',
            user='root',
            passwd='tigertiger',
            database='project'
        )


    def load_table_names(self):

        try:

            con = self.connect_db()

            cur = con.cursor()

            cur.execute("SHOW TABLES")

            tables = cur.fetchall()

            for table in tables:

                self.table_select.addItem(table[0])

            con.close()

        except Exception as e:

            print(e)

    def load_table(self):

        try:

            table_name = self.table_select.currentText()

            con = self.connect_db()

            cur = con.cursor()

            query = f"SELECT * FROM {table_name}"

            cur.execute(query)

            data = cur.fetchall()

            columns = cur.column_names

            self.table.setColumnCount(len(columns))
            self.table.setRowCount(len(data))

            self.table.setHorizontalHeaderLabels(columns)

            for row_index, row_data in enumerate(data):

                for col_index, value in enumerate(row_data):

                    item = QTableWidgetItem(str(value))

                    self.table.setItem(
                        row_index,
                        col_index,
                        item
                    )

            con.close()

        except Exception as e:

            QMessageBox.critical(self, "Error", str(e))

    def add_row(self):

        row_position = self.table.rowCount()

        self.table.insertRow(row_position)

    def delete_row(self):

        current_row = self.table.currentRow()

        if current_row >= 0:

            self.table.removeRow(current_row)
    def save_changes(self):

        try:

            table_name = self.table_select.currentText()

            con = self.connect_db()

            cur = con.cursor()


            cur.execute(f"DELETE FROM {table_name}")

            rows = self.table.rowCount()
            cols = self.table.columnCount()

            for row in range(rows):

                values = []

                for col in range(cols):

                    item = self.table.item(row, col)

                    if item is not None:

                        values.append(item.text())

                    else:

                        values.append("")

                formatted_values = []

                for value in values:

                    formatted_values.append(f"'{value}'")

                value_string = ",".join(formatted_values)

                query = f"""
                INSERT INTO {table_name}
                VALUES({value_string})
                """

                cur.execute(query)

            con.commit()

            QMessageBox.information(
                self,
                "Success",
                "Database updated successfully!"
            )

            con.close()

        except Exception as e:

            QMessageBox.critical(self, "Error", str(e))

app = QApplication(sys.argv)

window = DynamicDBMS()

window.show()

sys.exit(app.exec_())
