from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    """Response model for product information."""

    id: int
    name: str
    price: float
    inventory: int

    model_config = { "from_attributes": True }

class CartItemCreateSchema(BaseModel):
    """Request model for adding an item to the shopping cart."""

    session_id: str = Field(..., min_length=3)
    product_id: int = Field(..., gt=0)  
    quantity: int = Field(default=1, gt=0, le=10)

class CartItemSchema(BaseModel):
    """Response model for items in the shopping cart."""

    id: int
    session_id: str
    product_id: int
    quantity: int

    model_config = { "from_attributes": True }

class OrderCreateSchema(BaseModel):
    """Request model for placing an order."""

    session_id: str = Field(..., min_length=3)

class OrderSchema(BaseModel):
    """Response model for an order."""

    id: int
    session_id: str
    total_price: float
    message: str

    model_config = { "from_attributes": True }