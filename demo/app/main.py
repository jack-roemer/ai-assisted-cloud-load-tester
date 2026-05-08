from collections.abc import Generator
from contextlib import asynccontextmanager, contextmanager
import time

from fastapi import FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from demo.app.database import Base, SessionLocal, engine, get_db, DBSessionDependency
from demo.app.models import CartItemModel, OrderModel, ProductModel
from demo.app.schemas import *

@contextmanager
def db_session() -> Generator[Session, None, None]:
    """Context manager for database sessions."""

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to initialize database tables and seed product data."""

    Base.metadata.create_all(bind=engine)

    with db_session() as db:
        seed_products(db)

    yield


app = FastAPI(
    title="Load Tester Demo Store API",
    description="A simple API for a demo online store to be used as a target system for load testing.",
    version="1.0.0",
    lifespan=lifespan,
)


def seed_products(db: Session) -> None:
    """Seeds the database with initial product data."""

    if db.query(ProductModel).first():
        return

    products = [
        ProductModel(name="Cloud Architecture Handbook", price=39.99, inventory=50),
        ProductModel(name="Kubernetes Field Guide", price=44.99, inventory=35),
        ProductModel(name="Python Backend Patterns", price=34.99, inventory=40),
        ProductModel(name="AI Systems Notebook", price=24.99, inventory=75),
        ProductModel(name="Observability Starter Kit", price=29.99, inventory=25),
    ]

    db.add_all(products)
    db.commit()


@app.get("/health")
def health() -> dict[str, str]:
    """Returns API health status."""

    return { "status": "ok" }

@app.get("/products", response_model=list[ProductSchema])
def get_products(db: DBSessionDependency) -> list[ProductModel]:
    """Gets all products."""

    return db.query(ProductModel).all()

@app.get("/products/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: DBSessionDependency) -> ProductModel:
    """Gets a single product by ID."""

    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found",
        )

    return product


@app.post("/cart", response_model=CartItemSchema, status_code=status.HTTP_201_CREATED)
def create_cart_item(cart_item: CartItemCreateSchema, db: DBSessionDependency) -> CartItemModel:
    """Add an item to a user's cart."""

    product = db.query(ProductModel).filter(ProductModel.id == cart_item.product_id).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {cart_item.product_id} not found",
        )

    if product.inventory < cart_item.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not enough {product.id} in inventory, {product.inventory} left.",
        )

    cart_item = CartItemModel(
        session_id=cart_item.session_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item

@app.post("/checkout", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
def checkout(request: OrderCreateSchema, db: DBSessionDependency) -> OrderSchema:
    """
    Complete checkout for a session.

    This endpoint intentionally includes a short delay so future load tests
    can identify it as a slower endpoint.
    """

    time.sleep(0.25)

    cart_items = (db.query(CartItemModel).filter(CartItemModel.session_id == request.session_id).all())

    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cart {request.session_id} is empty",
        )

    total_price = 0.0

    for item in cart_items:
        product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()

        if product is None:
            continue

        total_price += product.price * item.quantity
        product.inventory -= item.quantity

    order = OrderModel(session_id=request.session_id, total_price=round(total_price, 2))

    db.add(order)

    for item in cart_items:
        db.delete(item)

    db.commit()
    db.refresh(order)

    return OrderSchema(
        id=order.id,
        session_id=order.session_id,
        total_price=order.total_price,
        message="Checkout completed successfully",
    )