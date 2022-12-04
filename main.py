import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from form_stuff import Ui_Form

STAFF_POSTS = ['бухгалтер', 'инженер', 'программист']


class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.conn = sqlite3.connect('stuff_db.db')
        self.setupUI(self)
        self.comboBox.addItems(STAFF_POSTS)
        self.pbOpen.clicked.connect(self.open_file)
        self.pbInsert.clicked.connect(self.insert_staff)

    def open_file(self):
        try:
            cur = self.conn.cursor()
            data = cur.execute("select * from stuff")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Ошибки при подключении к БД.{e}")
            return e
        self.twStuffs.setColumnCount(len(col_name))
        self.twStuffs.setHorizontalHeaderLabels(col_name)
        self.twStuffs.setRowCount(0)
        self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStuffs.setRowCount(self.twStuffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStuffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStuffs.resizeColumnsToContents()

    def insert_staff(self):
        row = [self.leFio.text(), self.sbAge.text(), 'муж' if self.rbMale.isChecked() else 'жен',
               self.lePhone.text(), self.leEmail.text(), self.comboBox.itemText(self.comboBox.currentIndex()),
               self.sbExp.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into stuff(fio, age, sex, phone, email, position, exp)
                values('{row[0]}', '{row[1]}', {row[2]}, '{row[3]}', '{row[4]}', '{row[5]}', {row[6]})""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStuffs()

    def update_twstuffs(self, query="select * from stuff"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStuffs.setRowCount(0)
        for i, row in enumerate(data):
            self.twStuffs.setRowCount(self.twStuffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStuffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStuffs.resizeColumnsToContents()

    def delete_staff(self):
        row = self.twStaffs.currentRow()
        num = self.twStaffs.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from staff where num = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twstuffs()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
