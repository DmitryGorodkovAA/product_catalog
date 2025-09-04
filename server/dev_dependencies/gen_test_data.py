import random
import psycopg2
from faker import Faker
from datetime import datetime

from infrastructure.config import Config


class TestDataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.conn = psycopg2.connect(
            dbname=Config.POSTGRES_DB,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD,
            host=Config.POSTGRES_HOST,
            port=Config.POSTGRES_PORT
        )
        self.cur = self.conn.cursor()

    def seed_catalog_containers(self, n=5):
        ids = []
        for _ in range(n):
            name = self.fake.word().capitalize() + " Container"
            description = self.fake.sentence()
            self.cur.execute("""
                INSERT INTO catalog_containers (name, description, is_active)
                VALUES (%s, %s, %s) RETURNING id;
            """, (name, description, True))
            ids.append(self.cur.fetchone()[0])
        return ids

    def seed_product_catalogs(self, containers, n=10):
        ids = []
        for _ in range(n):
            name = self.fake.word().capitalize() + " Catalog"
            description = self.fake.sentence()
            parent = random.choice(containers)
            self.cur.execute("""
                INSERT INTO product_catalogs (name, description, parent_container_id, is_active)
                VALUES (%s, %s, %s, %s) RETURNING id;
            """, (name, description, parent, True))
            ids.append(self.cur.fetchone()[0])
        return ids

    def seed_products(self, catalogs, n=50):
        ids = []
        for _ in range(n):
            name = self.fake.word().capitalize()
            description = self.fake.text(max_nb_chars=100)
            price = round(random.uniform(5, 500), 2)
            stock = random.randint(0, 100)
            catalog = random.choice(catalogs)
            self.cur.execute("""
                INSERT INTO products (name, description, price, stock, product_catalog_id, is_active)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """, (name, description, price, stock, catalog, True))
            ids.append(self.cur.fetchone()[0])
        return ids

    def seed_customers(self, n=20):
        ids = []
        for _ in range(n):
            if random.random() < 0.7:
                cust_type = "individual"
                name = self.fake.name()
                tax_id = None
            else:
                cust_type = "company"
                name = self.fake.company()
                tax_id = self.fake.ssn()

            self.cur.execute("""
                INSERT INTO customers (name, type, address, email, phone, tax_id, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """, (
                name,
                cust_type,
                self.fake.address(),
                self.fake.email(),
                self.fake.phone_number(),
                tax_id,
                True
            ))
            ids.append(self.cur.fetchone()[0])
        return ids

    def seed_orders(self, customers, n=30):
        ids = []
        statuses = ["new", "processing", "completed", "canceled"]
        for _ in range(n):
            cust = random.choice(customers)
            status = random.choice(statuses)
            self.cur.execute("""
                INSERT INTO orders (customer_id, status, delivery_address, notes)
                VALUES (%s, %s, %s, %s) RETURNING id;
            """, (
                cust,
                status,
                self.fake.address(),
                self.fake.sentence()
            ))
            ids.append(self.cur.fetchone()[0])
        return ids

    def seed_order_items(self, orders, products, n=100):
        for _ in range(n):
            order = random.choice(orders)
            product = random.choice(products)
            self.cur.execute("SELECT name, price FROM products WHERE id=%s;", (product,))
            product_name, price = self.cur.fetchone()
            quantity = random.randint(1, 5)
            self.cur.execute("""
                INSERT INTO order_items (order_id, product_id, product_name, unit_price, quantity, is_active)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                order,
                product,
                product_name,
                price,
                quantity,
                True
            ))

    def gen_test_data(self, nCatalogs:int, nProducts:int, nCustomers:int, nOrders:int, nOrderItems:int):
        containers = self.seed_catalog_containers()
        catalogs = self.seed_product_catalogs(containers, nCatalogs)
        products = self.seed_products(catalogs, nProducts)
        customers = self.seed_customers(nCustomers)
        orders = self.seed_orders(customers, nOrders)
        self.seed_order_items(orders, products, nOrderItems)

        self.conn.commit()
        self.cur.close()
        self.conn.close()

