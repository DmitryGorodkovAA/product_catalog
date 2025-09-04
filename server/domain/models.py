from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CatalogContainer:
    id: Optional[int]
    name: str
    parent_id: Optional[int]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool

@dataclass
class ProductCatalog:
    id: Optional[int]
    name: str
    parent_container_id: Optional[int]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool

@dataclass
class Product:
    id: Optional[int]
    name: str
    description: Optional[str]
    price: float
    stock: int
    reserved: int
    product_catalog_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    is_active: bool

    @property
    def available(self) -> int:
        return self.stock - self.reserved


@dataclass
class Customer:
    id: Optional[int]
    name: str
    type: str
    address: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    tax_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool


@dataclass
class Order:
    id: Optional[int]
    customer_id: Optional[int]
    order_date: datetime
    status: str
    delivery_address: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class OrderItem:
    id: Optional[int]
    order_id: int
    product_id: Optional[int]
    product_name: str
    unit_price: float
    quantity: int
    created_at: datetime
    is_active: bool
