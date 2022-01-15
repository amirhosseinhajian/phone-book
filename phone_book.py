import sqlite3
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtUiTools import QUiLoader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        self.ui = loader.load('main window.ui')
        self.ui.show()

        self.con = sqlite3.connect('database.db')
        self.my_cursor = self.con.cursor()

        self.number_of_contacts = 0
        self.load_data()

        self.ui.btn_add_new_contact.clicked.connect(self.add_new_contact)
        self.ui.delete_one_person_btn.clicked.connect(self.delete_person)
        self.ui.btn_delete_all_contacts.clicked.connect(self.delete_all)
        self.ui.dark_mode_btn.clicked.connect(self.dark_mode)
        self.ui.default_mode_btn.clicked.connect(self.default_mode)

    def load_data(self):
        try:
            self.my_cursor.execute("SELECT * FROM persons")
            result = self.my_cursor.fetchall()

            self.lay = QVBoxLayout()

            for item in result:
                labble = QLabel()
                self.number_of_contacts += 1
                labble.setText(str(self.number_of_contacts) + ") " + item[1] + " " + item[2] + ": " + item[4])
                self.my_cursor.execute(f"UPDATE persons SET id = '{self.number_of_contacts}' WHERE mobile_number = '{item[4]}'")
                self.con.commit()
                self.lay.addWidget(labble)
            self.ui.scrollContents.setLayout(self.lay)
            print("data loaded sucssusfully!")
        except:
            pass

    def add_new_contact(self):
        try:
            name = self.ui.name_box.text()
            family = self.ui.family_box.text()
            mobile_number = self.ui.mobile_number_box.text()
            self.ui.name_box.setText("")
            self.ui.family_box.setText("")
            self.ui.mobile_number_box.setText("")
            self.number_of_contacts += 1
            self.my_cursor.execute(f"INSERT INTO persons(id, name, family, mobile_number) VALUES('{self.number_of_contacts}', '{name}', '{family}', '{mobile_number}')")
            self.con.commit()
            labble = QLabel()
            labble.setText(str(self.number_of_contacts) + ") " + name + " " + family + ": " + mobile_number)
            self.lay.addWidget(labble)
            self.ui.scrollContents.setLayout(self.lay)
            print("New contact successfully added!")
        except:
            pass

    def delete_person(self):
        try:
            id = int(self.ui.id_box.text())
            self.ui.id_box.setText("")

            for i in range(self.lay.count()):
                if i == id - 1:
                    self.lay.itemAt(i).widget().deleteLater()

            self.ui.scrollContents.setLayout(self.lay)

            self.my_cursor.execute(f"DELETE FROM persons WHERE id == '{id}'")
            self.con.commit()
            print("Contact sucssusfully removed!")
        except:
            pass

    def delete_all(self):
        for i in range(self.lay.count()):
            self.lay.itemAt(i).widget().deleteLater()

        self.ui.scrollContents.setLayout(self.lay)
        self.my_cursor.execute("DELETE FROM persons")
        self.con.commit()
        self.number_of_contacts = 0
        print("All contact sucssusfully removed!")

    def dark_mode(self):
        self.ui.scrollArea.setStyleSheet("background-color: rgb(25, 25, 25); color: rgb(255, 255, 255);")
        # self.ui.label.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(25, 25, 25);")
        # self.ui.label_2.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(25, 25, 25);")
        # self.ui.name_box.setStyleSheet("background-color: rgb(25, 25, 25); color: rgb(255, 255, 255);")
        # self.ui.family_box.setStyleSheet("background-color: rgb(25, 25, 25); color: rgb(255, 255, 255);")
        # self.ui.mobile_number_box.setStyleSheet("background-color: rgb(25, 25, 25); color: rgb(255, 255, 255);")
        # self.ui.id_box.setStyleSheet("background-color: rgb(25, 25, 25); color: rgb(255, 255, 255);")

    def default_mode(self):
        self.ui.scrollArea.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        # self.ui.label.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);")
        # self.ui.label_2.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);")
        # self.ui.name_box.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        # self.ui.family_box.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        # self.ui.mobile_number_box.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        # self.ui.id_box.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")

app = QApplication()
main_window = MainWindow()
app.exec()
