from typing import Optional
from pydantic import Field, field_validator, validator
from app.api.schema import Base, CommonBase
from uuid import UUID
from datetime import datetime

from app.api.schema.categories.category_schema import CategoryRead

class ProductBase(Base):
    name: str
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    quantity: int =  Field(..., gt=0, description="quantity must be greater than 0")
    category_id:UUID


    # # sql alchemy constrain validation check
    # @field_validator("price",)
    # @classmethod
    # def validate_price(cls, price):
    #     if price<0:
    #         raise ValueError("price should greater then zero")
    #     return price

    
    # @field_validator("quantity",)
    # @classmethod
    # def validate_quantity(cls, quantity):
    #     if quantity<0:
    #         raise ValueError("quantity should greater then zero")
    #     return quantity


class ProductCreate(ProductBase):
    pass  # only input fields



class ProductRead(ProductBase, CommonBase):
    category: CategoryRead


    class Config:
        orm_mode = True  # important to read SQLAlchemy models
        fields = {
            'category_id': {'exclude': True}
        }