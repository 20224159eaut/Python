import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.uic import loadUi

from database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        
        # Load UI
        ui_path = os.path.join(os.path.dirname(__file__), 'ui', 'main_window.ui')
        loadUi(ui_path, self)
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        # Connect buttons
        self.btn_add_product.clicked.connect(self.add_product)
        self.btn_search_product.clicked.connect(self.search_products)
        
        self.btn_add_customer.clicked.connect(self.add_customer)
        self.btn_search_customer.clicked.connect(self.search_customers)
        
        self.btn_add_order.clicked.connect(self.add_order)
        self.btn_search_order.clicked.connect(self.search_orders)
        
        # Double click events
        self.table_orders.doubleClicked.connect(self.view_order_details)
    
    def load_data(self):
        self.load_products()
        self.load_customers()
        self.load_orders()
    
    # Product methods
    def load_products(self, data=None):
        if data is None:
            data = self.db.get_all_products()
        
        self.table_products.setRowCount(len(data))
        for row, product in enumerate(data):
            self.table_products.setItem(row, 0, QTableWidgetItem(product[0]))
            self.table_products.setItem(row, 1, QTableWidgetItem(product[1]))
            self.table_products.setItem(row, 2, QTableWidgetItem(f"{product[2]:,.0f}đ"))
            self.table_products.setItem(row, 3, QTableWidgetItem(product[3] or ""))
            
            # Add action buttons
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(5, 2, 5, 2)
            
            btn_edit = QPushButton("Sửa")
            btn_edit.setStyleSheet("background-color: #2196F3; color: white;")
            btn_edit.clicked.connect(lambda checked, p=product: self.edit_product(p))
            
            btn_delete = QPushButton("Xóa")
            btn_delete.setStyleSheet("background-color: #f44336; color: white;")
            btn_delete.clicked.connect(lambda checked, p=product: self.delete_product(p))
            
            btn_layout.addWidget(btn_edit)
            btn_layout.addWidget(btn_delete)
            self.table_products.setCellWidget(row, 4, btn_widget)
        
        self.table_products.resizeColumnsToContents()
    
    def search_products(self):
        keyword = self.lineEdit_search_product.text()
        search_type = self.combo_search_product.currentText()
        data = self.db.search_products(search_type, keyword)
        self.load_products(data)
    
    def add_product(self):
        dialog = ProductDialog(self.db, self)
        if dialog.exec():
            self.load_products()
            self.load_data()
    
    def edit_product(self, product):
        dialog = ProductDialog(self.db, self, product)
        if dialog.exec():
            self.load_products()
    
    def delete_product(self, product):
        reply = QMessageBox.question(self, 'Xác nhận', 
                                    f'Bạn có chắc muốn xóa mặt hàng {product[1]}?',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_product(product[0])
            self.load_products()
    
    # Customer methods
    def load_customers(self, data=None):
        if data is None:
            data = self.db.get_all_customers()
        
        self.table_customers.setRowCount(len(data))
        for row, customer in enumerate(data):
            self.table_customers.setItem(row, 0, QTableWidgetItem(customer[0]))
            self.table_customers.setItem(row, 1, QTableWidgetItem(customer[1]))
            self.table_customers.setItem(row, 2, QTableWidgetItem(customer[2] or ""))
            self.table_customers.setItem(row, 3, QTableWidgetItem(customer[3] or ""))
            
            # Add action buttons
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(5, 2, 5, 2)
            
            btn_edit = QPushButton("Sửa")
            btn_edit.setStyleSheet("background-color: #2196F3; color: white;")
            btn_edit.clicked.connect(lambda checked, c=customer: self.edit_customer(c))
            
            btn_delete = QPushButton("Xóa")
            btn_delete.setStyleSheet("background-color: #f44336; color: white;")
            btn_delete.clicked.connect(lambda checked, c=customer: self.delete_customer(c))
            
            btn_layout.addWidget(btn_edit)
            btn_layout.addWidget(btn_delete)
            self.table_customers.setCellWidget(row, 4, btn_widget)
        
        self.table_customers.resizeColumnsToContents()
    
    def search_customers(self):
        keyword = self.lineEdit_search_customer.text()
        search_type = self.combo_search_customer.currentText()
        data = self.db.search_customers(search_type, keyword)
        self.load_customers(data)
    
    def add_customer(self):
        dialog = CustomerDialog(self.db, self)
        if dialog.exec():
            self.load_customers()
            self.load_data()
    
    def edit_customer(self, customer):
        dialog = CustomerDialog(self.db, self, customer)
        if dialog.exec():
            self.load_customers()
    
    def delete_customer(self, customer):
        reply = QMessageBox.question(self, 'Xác nhận', 
                                    f'Bạn có chắc muốn xóa khách hàng {customer[1]}?',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_customer(customer[0])
            self.load_customers()
    
    # Order methods
    def load_orders(self, data=None):
        if data is None:
            data = self.db.get_all_orders()
        
        self.table_orders.setRowCount(len(data))
        for row, order in enumerate(data):
            self.table_orders.setItem(row, 0, QTableWidgetItem(order[0]))
            self.table_orders.setItem(row, 1, QTableWidgetItem(order[1]))
            self.table_orders.setItem(row, 2, QTableWidgetItem(order[2]))
            self.table_orders.setItem(row, 3, QTableWidgetItem(f"{order[3]:,.0f}đ"))
            
            # Add action buttons
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(5, 2, 5, 2)
            
            btn_edit = QPushButton("Sửa")
            btn_edit.setStyleSheet("background-color: #2196F3; color: white;")
            btn_edit.clicked.connect(lambda checked, o=order: self.edit_order(o))
            
            btn_delete = QPushButton("Xóa")
            btn_delete.setStyleSheet("background-color: #f44336; color: white;")
            btn_delete.clicked.connect(lambda checked, o=order: self.delete_order(o))
            
            btn_layout.addWidget(btn_edit)
            btn_layout.addWidget(btn_delete)
            self.table_orders.setCellWidget(row, 4, btn_widget)
        
        self.table_orders.resizeColumnsToContents()
    
    def search_orders(self):
        keyword = self.lineEdit_search_order.text()
        search_type = self.combo_search_order.currentText()
        data = self.db.search_orders(search_type, keyword)
        self.load_orders(data)
    
    def add_order(self):
        dialog = OrderDialog(self.db, self)
        if dialog.exec():
            self.load_orders()
    
    def edit_order(self, order):
        dialog = OrderDialog(self.db, self, order)
        if dialog.exec():
            self.load_orders()
    
    def delete_order(self, order):
        reply = QMessageBox.question(self, 'Xác nhận', 
                                    f'Bạn có chắc muốn xóa đơn hàng {order[0]}?',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_order(order[0])
            self.load_orders()
    
    def view_order_details(self, index):
        order_code = self.table_orders.item(index.row(), 0).text()
        dialog = OrderDetailDialog(self.db, order_code, self)
        dialog.exec()


class ProductDialog(QDialog):
    def __init__(self, db, parent=None, product=None):
        super().__init__(parent)
        self.db = db
        self.product = product
        
        ui_path = os.path.join(os.path.dirname(__file__), 'ui', 'product_dialog.ui')
        loadUi(ui_path, self)
        
        self.setup_ui()
    
    def setup_ui(self):
        if self.product:
            self.setWindowTitle("Sửa mặt hàng")
            self.lineEdit_code.setText(self.product[0])
            self.lineEdit_code.setEnabled(False)
            self.lineEdit_name.setText(self.product[1])
            self.spinBox_price.setValue(self.product[2])
            self.lineEdit_origin.setText(self.product[3] or "")
    
    def accept(self):
        code = self.lineEdit_code.text()
        name = self.lineEdit_name.text()
        price = self.spinBox_price.value()
        origin = self.lineEdit_origin.text()
        
        if not code or not name:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        if self.product:
            self.db.update_product(code, name, price, origin)
        else:
            if not self.db.add_product(code, name, price, origin):
                QMessageBox.warning(self, "Cảnh báo", "Mã hàng đã tồn tại!")
                return
        
        super().accept()


class CustomerDialog(QDialog):
    def __init__(self, db, parent=None, customer=None):
        super().__init__(parent)
        self.db = db
        self.customer = customer
        
        ui_path = os.path.join(os.path.dirname(__file__), 'ui', 'customer_dialog.ui')
        loadUi(ui_path, self)
        
        self.setup_ui()
    
    def setup_ui(self):
        if self.customer:
            self.setWindowTitle("Sửa khách hàng")
            self.lineEdit_code.setText(self.customer[0])
            self.lineEdit_code.setEnabled(False)
            self.lineEdit_name.setText(self.customer[1])
            self.lineEdit_address.setText(self.customer[2] or "")
            self.lineEdit_phone.setText(self.customer[3] or "")
    
    def accept(self):
        code = self.lineEdit_code.text()
        name = self.lineEdit_name.text()
        address = self.lineEdit_address.text()
        phone = self.lineEdit_phone.text()
        
        if not code or not name:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        if self.customer:
            self.db.update_customer(code, name, address, phone)
        else:
            if not self.db.add_customer(code, name, address, phone):
                QMessageBox.warning(self, "Cảnh báo", "Mã khách hàng đã tồn tại!")
                return
        
        super().accept()


class OrderDialog(QDialog):
    def __init__(self, db, parent=None, order=None):
        super().__init__(parent)
        self.db = db
        self.order = order
        self.order_details = []
        
        ui_path = os.path.join(os.path.dirname(__file__), 'ui', 'order_dialog.ui')
        loadUi(ui_path, self)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Load customers to combo box
        customers = self.db.get_all_customers()
        for customer in customers:
            self.combo_customer_code.addItem(f"{customer[0]} - {customer[1]}", customer[0])
        
        self.dateEdit.setDate(QDate.currentDate())
        
        self.btn_add_product.clicked.connect(self.add_product)
        
        if self.order:
            self.setWindowTitle("Sửa đơn hàng")
            self.lineEdit_order_code.setText(self.order[0])
            self.lineEdit_order_code.setEnabled(False)
            
            # Find customer in combo
            index = self.combo_customer_code.findData(self.order[1])
            if index >= 0:
                self.combo_customer_code.setCurrentIndex(index)
            
            date = QDate.fromString(self.order[2], "yyyy-MM-dd")
            self.dateEdit.setDate(date)
            
            # Load order details
            self.order_details = self.db.get_order_details(self.order[0])
            self.load_order_details()
    
    def load_order_details(self):
        self.table_order_details.setRowCount(len(self.order_details))
        total = 0
        for row, detail in enumerate(self.order_details):
            self.table_order_details.setItem(row, 0, QTableWidgetItem(detail[0]))
            self.table_order_details.setItem(row, 1, QTableWidgetItem(detail[1]))
            self.table_order_details.setItem(row, 2, QTableWidgetItem(str(detail[2])))
            self.table_order_details.setItem(row, 3, QTableWidgetItem(f"{detail[3]:,.0f}đ"))
            self.table_order_details.setItem(row, 4, QTableWidgetItem(f"{detail[4]:,.0f}đ"))
            
            # Add delete button
            btn_delete = QPushButton("Xóa")
            btn_delete.setStyleSheet("background-color: #f44336; color: white;")
            btn_delete.clicked.connect(lambda checked, r=row: self.delete_order_detail(r))
            
            self.table_order_details.setCellWidget(row, 5, btn_delete)
            total += detail[4]
        
        self.label_total.setText(f"Tổng tiền: {total:,.0f}đ")
        self.table_order_details.resizeColumnsToContents()
    
    def delete_order_detail(self, row):
        reply = QMessageBox.question(self, 'Xác nhận', 
                                    'Bạn có chắc muốn xóa mặt hàng này?',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.order_details.pop(row)
            self.load_order_details()
    
    def add_product(self):
        dialog = SelectProductDialog(self.db, self)
        if dialog.exec():
            product_code, quantity = dialog.get_selected_product()
            product = self.db.get_product(product_code)
            
            # Check if product already in order
            for i, detail in enumerate(self.order_details):
                if detail[0] == product_code:
                    # Update quantity
                    new_quantity = detail[2] + quantity
                    self.order_details[i] = (detail[0], detail[1], new_quantity, detail[3], new_quantity * detail[3])
                    self.load_order_details()
                    return
            
            # Add new product
            total = quantity * product[2]
            self.order_details.append((product[0], product[1], quantity, product[2], total))
            self.load_order_details()
    
    def accept(self):
        order_code = self.lineEdit_order_code.text()
        customer_code = self.combo_customer_code.currentData()
        order_date = self.dateEdit.date().toString("yyyy-MM-dd")
        
        if not order_code:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập mã đơn hàng!")
            return
        
        if not self.order_details:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng thêm mặt hàng vào đơn hàng!")
            return
        
        if self.order:
            self.db.update_order(order_code, customer_code, order_date)
            self.db.clear_order_details(order_code)
        else:
            if not self.db.add_order(order_code, customer_code, order_date):
                QMessageBox.warning(self, "Cảnh báo", "Mã đơn hàng đã tồn tại!")
                return
        
        # Add order details
        for detail in self.order_details:
            self.db.add_order_detail(order_code, detail[0], detail[2], detail[3])
        
        super().accept()


class SelectProductDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.selected_product = None
        self.selected_quantity = 1
        
        ui_path = os.path.join(os.path.dirname(__file__), 'ui', 'select_product_dialog.ui')
        loadUi(ui_path, self)
        
        self.setup_ui()
    
    def setup_ui(self):
        self.load_products()
        self.btn_search.clicked.connect(self.search_products)
        self.btn_select.clicked.connect(self.select_product)
        self.btn_cancel.clicked.connect(self.reject)
        self.table_products.doubleClicked.connect(self.select_product)
    
    def load_products(self, data=None):
        if data is None:
            data = self.db.get_all_products()
        
        self.table_products.setRowCount(len(data))
        for row, product in enumerate(data):
            self.table_products.setItem(row, 0, QTableWidgetItem(product[0]))
            self.table_products.setItem(row, 1, QTableWidgetItem(product[1]))
            self.table_products.setItem(row, 2, QTableWidgetItem(f"{product[2]:,.0f}đ"))
            self.table_products.setItem(row, 3, QTableWidgetItem(product[3] or ""))
        
        self.table_products.resizeColumnsToContents()
    
    def search_products(self):
        keyword = self.lineEdit_search.text()
        data = self.db.search_products("Tất cả", keyword)
        self.load_products(data)
    
    def select_product(self):
        current_row = self.table_products.currentRow()
        if current_row >= 0:
            self.selected_product = self.table_products.item(current_row, 0).text()
            self.selected_quantity = self.spinBox_quantity.value()
            self.accept()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn mặt hàng!")
    
    def get_selected_product(self):
        return self.selected_product, self.selected_quantity


class OrderDetailDialog(QDialog):
    def __init__(self, db, order_code, parent=None):
        super().__init__(parent)
        self.db = db
        self.order_code = order_code
        
        self.setWindowTitle(f"Chi tiết đơn hàng {order_code}")
        self.resize(800, 500)
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Mã hàng", "Tên hàng", "Số lượng", "Đơn giá", "Thành tiền"])
        
        layout.addWidget(self.table)
        
        # Total label
        self.label_total = QLabel()
        self.label_total.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.label_total.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        layout.addWidget(self.label_total)
        
        # Close button
        btn_close = QPushButton("Đóng")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        
        self.setLayout(layout)
    
    def load_data(self):
        details = self.db.get_order_details(self.order_code)
        total = 0
        
        self.table.setRowCount(len(details))
        for row, detail in enumerate(details):
            self.table.setItem(row, 0, QTableWidgetItem(detail[0]))
            self.table.setItem(row, 1, QTableWidgetItem(detail[1]))
            self.table.setItem(row, 2, QTableWidgetItem(str(detail[2])))
            self.table.setItem(row, 3, QTableWidgetItem(f"{detail[3]:,.0f}đ"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{detail[4]:,.0f}đ"))
            total += detail[4]
        
        self.label_total.setText(f"Tổng tiền: {total:,.0f}đ")
        self.table.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())