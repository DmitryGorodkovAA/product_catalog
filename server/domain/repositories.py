from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Product, Order, OrderItem, Customer


class ProductRepository(ABC):

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def update(self, product: Product) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[Product]:
        pass


class CustomerRepository(ABC):

    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    def list_all(self) -> List[Customer]:
        pass

    @abstractmethod
    def add(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def update(self, customer: Customer) -> None:
        pass

class OrderRepository(ABC):

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def add(self, order: Order) -> Order:
        pass

    @abstractmethod
    def update(self, order: Order) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[Order]:
        pass


class OrderItemRepository(ABC):

    @abstractmethod
    def list_by_order(self, order_id: int) -> List[OrderItem]:
        pass

    @abstractmethod
    def get_by_order_and_product(self, order_id: int, product_id: int) -> Optional[OrderItem]:
        pass

    @abstractmethod
    def add(self, order_item: OrderItem) -> OrderItem:
        pass

    @abstractmethod
    def update(self, order_item: OrderItem) -> None:
        pass
