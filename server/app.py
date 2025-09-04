from flask import Flask, request, jsonify
from datetime import datetime

from infrastructure.config import Config
from infrastructure.repositories.postgresql_repositories import PostgresConnection
from infrastructure.repositories.postgresql_repositories import (
    PostgresConnection,
    PostgresProductRepository,
    PostgresOrderRepository,
    PostgresOrderItemRepository
)
from usecases.add_product_to_order import OrderService, OrderNotFoundError, ProductNotFoundError, InsufficientStockError
from dev_dependencies.gen_test_data import TestDataGenerator
app = Flask(__name__)

connection = PostgresConnection()

product_repo = PostgresProductRepository(connection)
order_repo = PostgresOrderRepository(connection)
order_item_repo = PostgresOrderItemRepository(connection)

order_service = OrderService(
    product_repo=product_repo,
    order_repo=order_repo,
    order_item_repo=order_item_repo
)


@app.route("/orders/<int:order_id>/items", methods=["POST"])
def add_product_to_order(order_id):
    data = request.get_json()
    if not data:
        return jsonify({"detail": "Request body must be JSON"}), 400

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not isinstance(product_id, int) or not isinstance(quantity, int):
        return jsonify({"detail": "product_id and quantity must be integers"}), 400
    if quantity <= 0:
        return jsonify({"detail": "quantity must be positive"}), 400

    try:
        order_item = order_service.add_product_to_order(order_id, product_id, quantity)
        return jsonify({
            "id": order_item.id,
            "order_id": order_item.order_id,
            "product_id": order_item.product_id,
            "product_name": order_item.product_name,
            "unit_price": order_item.unit_price,
            "quantity": order_item.quantity,
            "created_at": order_item.created_at.isoformat(),
            "is_active": order_item.is_active
        })
    except OrderNotFoundError:
        return jsonify({"detail": f"Order {order_id} not found"}), 404
    except ProductNotFoundError:
        return jsonify({"detail": f"Product {product_id} not found"}), 404
    except InsufficientStockError as e:
        return jsonify({"detail": str(e)}), 400
    except Exception as e:
        return jsonify({"detail": f"Internal server error: {str(e)}"}), 500

@app.route("/dev/gen_test_story", methods=["POST"])
def generate_test_data():
    data = request.get_json()
    if not data:
        return jsonify({"detail": "Request body must be JSON"}), 400

    nCatalogs = data.get("n_catalogs")
    nProducts = data.get("n_products")
    nCustomers = data.get("n_customers")
    nOrders = data.get("n_orders")
    nOrderItems = data.get("n_order_items")

    if not nCatalogs or not nProducts or not nCustomers or not nOrders or not nOrderItems:
        return jsonify({"detail": "Request body must be JSON"}), 400

    try:
        int(nCatalogs)
        int(nProducts)
        int(nCustomers)
        int(nOrders)
        int(nOrderItems)
    except ValueError:
        return jsonify({"detail": "The values do not meet the requirements"}), 400

    try:
        testDataGenerator = TestDataGenerator()

        testDataGenerator.gen_test_data(nCatalogs, nProducts, nCustomers, nOrders, nOrderItems)
        return jsonify({"detail": "Test data generated"}), 200
    except Exception as e:
        return jsonify({"detail": str(e)}), 400



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=Config.FLASK_PORT)
