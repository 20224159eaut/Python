import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('quanly_banhang.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Bảng mặt hàng
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                code TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                origin TEXT
            )
        ''')
        
        # Bảng khách hàng
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                code TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT
            )
        ''')
        
        # Bảng đơn hàng
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                code TEXT PRIMARY KEY,
                customer_code TEXT,
                order_date TEXT,
                FOREIGN KEY (customer_code) REFERENCES customers(code)
            )
        ''')
        
        # Bảng chi tiết đơn hàng
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_code TEXT,
                product_code TEXT,
                quantity INTEGER,
                price REAL,
                FOREIGN KEY (order_code) REFERENCES orders(code),
                FOREIGN KEY (product_code) REFERENCES products(code)
            )
        ''')
        
        self.conn.commit()
    
    # Product methods
    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products ORDER BY code")
        return self.cursor.fetchall()
    
    def search_products(self, search_type, keyword):
        if search_type == "Mã hàng":
            self.cursor.execute("SELECT * FROM products WHERE code LIKE ?", (f'%{keyword}%',))
        elif search_type == "Tên hàng":
            self.cursor.execute("SELECT * FROM products WHERE name LIKE ?", (f'%{keyword}%',))
        elif search_type == "Nguồn gốc":
            self.cursor.execute("SELECT * FROM products WHERE origin LIKE ?", (f'%{keyword}%',))
        else:
            self.cursor.execute("SELECT * FROM products WHERE code LIKE ? OR name LIKE ? OR origin LIKE ?", 
                              (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        return self.cursor.fetchall()
    
    def add_product(self, code, name, price, origin):
        try:
            self.cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?)", 
                              (code, name, price, origin))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_product(self, code, name, price, origin):
        self.cursor.execute("UPDATE products SET name=?, price=?, origin=? WHERE code=?", 
                          (name, price, origin, code))
        self.conn.commit()
    
    def delete_product(self, code):
        self.cursor.execute("DELETE FROM products WHERE code=?", (code,))
        self.conn.commit()
    
    def get_product(self, code):
        self.cursor.execute("SELECT * FROM products WHERE code=?", (code,))
        return self.cursor.fetchone()
    
    # Customer methods
    def get_all_customers(self):
        self.cursor.execute("SELECT * FROM customers ORDER BY code")
        return self.cursor.fetchall()
    
    def search_customers(self, search_type, keyword):
        if search_type == "Mã khách":
            self.cursor.execute("SELECT * FROM customers WHERE code LIKE ?", (f'%{keyword}%',))
        elif search_type == "Tên khách":
            self.cursor.execute("SELECT * FROM customers WHERE name LIKE ?", (f'%{keyword}%',))
        elif search_type == "Địa chỉ":
            self.cursor.execute("SELECT * FROM customers WHERE address LIKE ?", (f'%{keyword}%',))
        elif search_type == "Số điện thoại":
            self.cursor.execute("SELECT * FROM customers WHERE phone LIKE ?", (f'%{keyword}%',))
        else:
            self.cursor.execute("SELECT * FROM customers WHERE code LIKE ? OR name LIKE ? OR address LIKE ? OR phone LIKE ?",
                              (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        return self.cursor.fetchall()
    
    def add_customer(self, code, name, address, phone):
        try:
            self.cursor.execute("INSERT INTO customers VALUES (?, ?, ?, ?)", 
                              (code, name, address, phone))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_customer(self, code, name, address, phone):
        self.cursor.execute("UPDATE customers SET name=?, address=?, phone=? WHERE code=?", 
                          (name, address, phone, code))
        self.conn.commit()
    
    def delete_customer(self, code):
        self.cursor.execute("DELETE FROM customers WHERE code=?", (code,))
        self.conn.commit()
    
    def get_customer(self, code):
        self.cursor.execute("SELECT * FROM customers WHERE code=?", (code,))
        return self.cursor.fetchone()
    
    # Order methods
    def get_all_orders(self):
        self.cursor.execute("""
            SELECT o.code, o.customer_code, o.order_date, 
                   COALESCE(SUM(od.quantity * od.price), 0) as total
            FROM orders o
            LEFT JOIN order_details od ON o.code = od.order_code
            GROUP BY o.code
            ORDER BY o.order_date DESC
        """)
        return self.cursor.fetchall()
    
    def search_orders(self, search_type, keyword):
        if search_type == "Mã đơn hàng":
            self.cursor.execute("""
                SELECT o.code, o.customer_code, o.order_date, 
                       COALESCE(SUM(od.quantity * od.price), 0) as total
                FROM orders o
                LEFT JOIN order_details od ON o.code = od.order_code
                WHERE o.code LIKE ?
                GROUP BY o.code
            """, (f'%{keyword}%',))
        else:  # Mã khách hàng
            self.cursor.execute("""
                SELECT o.code, o.customer_code, o.order_date, 
                       COALESCE(SUM(od.quantity * od.price), 0) as total
                FROM orders o
                LEFT JOIN order_details od ON o.code = od.order_code
                WHERE o.customer_code LIKE ?
                GROUP BY o.code
            """, (f'%{keyword}%',))
        return self.cursor.fetchall()
    
    def add_order(self, code, customer_code, order_date):
        try:
            self.cursor.execute("INSERT INTO orders VALUES (?, ?, ?)", 
                              (code, customer_code, order_date))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_order(self, code, customer_code, order_date):
        self.cursor.execute("UPDATE orders SET customer_code=?, order_date=? WHERE code=?", 
                          (customer_code, order_date, code))
        self.conn.commit()
    
    def delete_order(self, code):
        # Xóa chi tiết đơn hàng trước
        self.cursor.execute("DELETE FROM order_details WHERE order_code=?", (code,))
        self.cursor.execute("DELETE FROM orders WHERE code=?", (code,))
        self.conn.commit()
    
    def get_order(self, code):
        self.cursor.execute("SELECT * FROM orders WHERE code=?", (code,))
        return self.cursor.fetchone()
    
    def get_order_details(self, order_code):
        self.cursor.execute("""
            SELECT od.product_code, p.name, od.quantity, od.price, 
                   od.quantity * od.price as total
            FROM order_details od
            JOIN products p ON od.product_code = p.code
            WHERE od.order_code = ?
        """, (order_code,))
        return self.cursor.fetchall()
    
    def add_order_detail(self, order_code, product_code, quantity, price):
        self.cursor.execute("""
            INSERT INTO order_details (order_code, product_code, quantity, price)
            VALUES (?, ?, ?, ?)
        """, (order_code, product_code, quantity, price))
        self.conn.commit()
    
    def delete_order_detail(self, order_code, product_code):
        self.cursor.execute("""
            DELETE FROM order_details 
            WHERE order_code=? AND product_code=?
        """, (order_code, product_code))
        self.conn.commit()
    
    def clear_order_details(self, order_code):
        self.cursor.execute("DELETE FROM order_details WHERE order_code=?", (order_code,))
        self.conn.commit()
    
    def close(self):
        self.conn.close()