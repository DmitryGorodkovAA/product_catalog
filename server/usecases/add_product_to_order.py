from datetime import datetime
from domain.models import OrderItem
from domain.repositories import ProductRepository, OrderRepository, OrderItemRepository

class OrderNotFoundError(Exception): pass
class ProductNotFoundError(Exception): pass
class InsufficientStockError(Exception): pass


class OrderService:
    def __init__(
        self,
        product_repo: ProductRepository,
        order_repo: OrderRepository,
        order_item_repo: OrderItemRepository
    ):
        self.product_repo = product_repo
        self.order_repo = order_repo
        self.order_item_repo = order_item_repo

    def add_product_to_order(self, order_id: int, product_id: int, quantity: int) -> OrderItem:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise OrderNotFoundError(f"Order {order_id} not found")

        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product {product_id} not found")

        if product.available < quantity:
            raise InsufficientStockError(
                f"Not enough stock for product {product_id}: available {product.available}, requested {quantity}"
            )

        order_item = self.order_item_repo.get_by_order_and_product(order_id, product_id)

        if order_item:
            order_item.quantity += quantity
            self.order_item_repo.update(order_item)
        else:
            order_item = OrderItem(
                id=None,
                order_id=order_id,
                product_id=product_id,
                product_name=product.name,
                unit_price=product.price,
                quantity=quantity,
                created_at=datetime.utcnow(),
                is_active=True
            )
            order_item = self.order_item_repo.add(order_item)

        product.reserved += quantity
        self.product_repo.update(product)

        return order_item
