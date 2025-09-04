from typing import List, Optional
from abc import ABC
from domain.models import Product, Customer, Order, OrderItem
from domain.repositories import ProductRepository, CustomerRepository, OrderRepository, OrderItemRepository
from infrastructure.config import Config
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime


class PostgresConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=Config.POSTGRES_DB,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD,
            host=Config.POSTGRES_HOST,
            port=Config.POSTGRES_PORT
        )

    def cursor(self):
        return self.conn.cursor(cursor_factory=RealDictCursor)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


class PostgresProductRepository(ProductRepository):
    def __init__(self, connection: PostgresConnection):
        self.connection = connection

    def get_by_id(self, product_id: int) -> Optional[Product]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        row = cur.fetchone()
        cur.close()
        if row:
            return Product(**row)
        return None

    def update(self, product: Product) -> None:
        cur = self.connection.cursor()
        cur.execute(
            """
            UPDATE products
            SET name=%s, description=%s, price=%s, stock=%s, reserved=%s, product_catalog_id=%s,
                updated_at=%s, is_active=%s
            WHERE id=%s
            """,
            (
                product.name, product.description, product.price, product.stock,
                product.reserved, product.product_catalog_id, datetime.utcnow(), product.is_active, product.id
            )
        )
        self.connection.commit()
        cur.close()

    def list_all(self) -> List[Product]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        cur.close()
        return [Product(**row) for row in rows]


class PostgresCustomerRepository(CustomerRepository):
    def __init__(self, connection: PostgresConnection):
        self.connection = connection

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        row = cur.fetchone()
        cur.close()
        if row:
            return Customer(**row)
        return None

    def list_all(self) -> List[Customer]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM customers")
        rows = cur.fetchall()
        cur.close()
        return [Customer(**row) for row in rows]

    def add(self, customer: Customer) -> Customer:
        cur = self.connection.cursor()
        cur.execute(
            """
            INSERT INTO customers (name, type, address, email, phone, tax_id, created_at, updated_at, is_active)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING *
            """,
            (
                customer.name, customer.type, customer.address, customer.email,
                customer.phone, customer.tax_id, customer.created_at,
                customer.updated_at, customer.is_active
            )
        )
        row = cur.fetchone()
        self.connection.commit()
        cur.close()
        return Customer(**row)

    def update(self, customer: Customer) -> None:
        cur = self.connection.cursor()
        cur.execute(
            """
            UPDATE customers
            SET name=%s, type=%s, address=%s, email=%s, phone=%s, tax_id=%s, updated_at=%s, is_active=%s
            WHERE id=%s
            """,
            (
                customer.name, customer.type, customer.address, customer.email,
                customer.phone, customer.tax_id, datetime.utcnow(), customer.is_active, customer.id
            )
        )
        self.connection.commit()
        cur.close()


class PostgresOrderRepository(OrderRepository):
    def __init__(self, connection: PostgresConnection):
        self.connection = connection

    def get_by_id(self, order_id: int) -> Optional[Order]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        row = cur.fetchone()
        cur.close()
        if row:
            return Order(**row)
        return None

    def add(self, order: Order) -> Order:
        cur = self.connection.cursor()
        cur.execute(
            """
            INSERT INTO orders (customer_id, order_date, status, delivery_address, notes, created_at, updated_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING *
            """,
            (
                order.customer_id, order.order_date, order.status, order.delivery_address,
                order.notes, order.created_at, order.updated_at
            )
        )
        row = cur.fetchone()
        self.connection.commit()
        cur.close()
        return Order(**row)

    def update(self, order: Order) -> None:
        cur = self.connection.cursor()
        cur.execute(
            """
            UPDATE orders
            SET customer_id=%s, order_date=%s, status=%s, delivery_address=%s, notes=%s, updated_at=%s
            WHERE id=%s
            """,
            (
                order.customer_id, order.order_date, order.status,
                order.delivery_address, order.notes, datetime.utcnow(), order.id
            )
        )
        self.connection.commit()
        cur.close()

    def list_all(self) -> List[Order]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM orders")
        rows = cur.fetchall()
        cur.close()
        return [Order(**row) for row in rows]


class PostgresOrderItemRepository(OrderItemRepository):
    def __init__(self, connection: PostgresConnection):
        self.connection = connection

    def list_by_order(self, order_id: int) -> List[OrderItem]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
        rows = cur.fetchall()
        cur.close()
        return [OrderItem(**row) for row in rows]

    def get_by_order_and_product(self, order_id: int, product_id: int) -> Optional[OrderItem]:
        cur = self.connection.cursor()
        cur.execute(
            "SELECT * FROM order_items WHERE order_id = %s AND product_id = %s",
            (order_id, product_id)
        )
        row = cur.fetchone()
        cur.close()
        if row:
            return OrderItem(**row)
        return None

    def add(self, order_item: OrderItem) -> OrderItem:
        cur = self.connection.cursor()
        cur.execute(
            """
            INSERT INTO order_items (order_id, product_id, product_name, unit_price, quantity, created_at, is_active)
            VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING *
            """,
            (
                order_item.order_id, order_item.product_id, order_item.product_name,
                order_item.unit_price, order_item.quantity, order_item.created_at, order_item.is_active
            )
        )
        row = cur.fetchone()
        self.connection.commit()
        cur.close()
        return OrderItem(**row)

    def update(self, order_item: OrderItem) -> None:
        cur = self.connection.cursor()
        cur.execute(
            """
            UPDATE order_items
            SET quantity=%s, is_active=%s
            WHERE id=%s
            """,
            (order_item.quantity, order_item.is_active, order_item.id)
        )
        self.connection.commit()
        cur.close()
