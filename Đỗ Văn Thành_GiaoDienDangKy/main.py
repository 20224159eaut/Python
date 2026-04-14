import sys
import re
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton, QHBoxLayout, QWidget

class MemberApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Nạp file giao diện .ui
        uic.loadUi("registration.ui", self)
        
        self.init_db()
        self.setup_connections()
        self.load_data()

    def init_db(self):
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ho TEXT, ten TEXT, contact TEXT, pwd TEXT, dob TEXT, gender TEXT
            )
        """)
        self.conn.commit()

    def setup_connections(self):
        self.btn_register.clicked.connect(self.handle_register)
        self.btn_back.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

    def validate_pwd(self, pwd):
        # Yêu cầu: 8 ký tự, 1 a-z, 1 A-Z, 1 số, 1 ký tự đặc biệt
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        return re.match(pattern, pwd)

    def handle_register(self):
        ho = self.txt_ho.text()
        ten = self.txt_ten.text()
        contact = self.txt_contact.text()
        pwd = self.txt_password.text()
        dob = self.date_birth.date().toString("dd/MM/yyyy")
        gender = "Nam" if self.radio_nam.isChecked() else "Nữ" if self.radio_nu.isChecked() else ""

        # Kiểm tra trống & checkbox
        if not all([ho, ten, contact, pwd, gender]) or not self.chk_agree.isChecked():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đủ thông tin và đồng ý điều khoản!")
            return

        # Kiểm tra mật khẩu
        if not self.validate_pwd(pwd):
            QMessageBox.critical(self, "Lỗi", "Mật khẩu yếu! Cần ít nhất 8 ký tự, 1 chữ hoa, 1 chữ thường, 1 số và 1 ký tự đặc biệt.")
            return

        # Lưu Database
        self.cursor.execute("INSERT INTO members (ho, ten, contact, pwd, dob, gender) VALUES (?,?,?,?,?,?)",
                            (ho, ten, contact, pwd, dob, gender))
        self.conn.commit()
        
        QMessageBox.information(self, "Thông báo", "Đăng ký thành công!")
        self.load_data()
        self.stackedWidget.setCurrentIndex(1) # Chuyển sang trang danh sách

    def load_data(self):
        self.cursor.execute("SELECT * FROM members")
        rows = self.cursor.fetchall()
        
        self.table_members.setColumnCount(6)
        self.table_members.setHorizontalHeaderLabels(["ID", "Họ Tên", "Liên hệ", "Ngày sinh", "Giới tính", "Thao tác"])
        self.table_members.setRowCount(0)

        for row_idx, row_data in enumerate(rows):
            self.table_members.insertRow(row_idx)
            self.table_members.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
            self.table_members.setItem(row_idx, 1, QTableWidgetItem(f"{row_data[1]} {row_data[2]}"))
            self.table_members.setItem(row_idx, 2, QTableWidgetItem(row_data[3]))
            self.table_members.setItem(row_idx, 3, QTableWidgetItem(row_data[5]))
            self.table_members.setItem(row_idx, 4, QTableWidgetItem(row_data[6]))

            # Nút Xóa
            btn_del = QPushButton("Xóa")
            btn_del.setStyleSheet("background-color: #ff4d4d; color: white;")
            btn_del.clicked.connect(lambda _, id=row_data[0]: self.delete_member(id))
            self.table_members.setCellWidget(row_idx, 5, btn_del)

    def delete_member(self, member_id):
        confirm = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn xóa?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.cursor.execute("DELETE FROM members WHERE id=?", (member_id,))
            self.conn.commit()
            self.load_data()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MemberApp()
    window.show()
    sys.exit(app.exec())