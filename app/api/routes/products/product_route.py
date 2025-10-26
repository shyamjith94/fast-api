from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from app.api.schema import ProductRead, ProductCreate
from app.api.models import Product
from app.api.depends import Database
from sqlalchemy.orm import joinedload, defer


product_router = APIRouter(prefix="/product")
db_class = Database()



@product_router.get("/", response_model=List[ProductRead],)
def get_products(*, db: Database = Depends(db_class.get_db)):
    try:
        products = db.query(Product).options( joinedload(Product.category),).all()
        return products
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

# get product by id


@product_router.get("/{id}", response_model=ProductRead,)
def get_product(*, id: int):
    return {}

# create product


@product_router.post("/", response_model=ProductRead,)
def create_product(
    *,
    prod_in: ProductCreate,
    db:Database =Depends(db_class.get_db)
):
    try:
        new_product = Product(**prod_in.model_dump())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(),)

# partial update product


@product_router.patch("/{id}", response_model=ProductRead,)
def create_product(
    *,
    prod_in: ProductCreate,
    id: int
):
   
    return {}

# update product


@product_router.put("/{id}", response_model=ProductRead,)
def create_product(
    *,
    prod_in: ProductRead,
    id: int
):
   
    return {}


# delete product
@product_router.delete("/{id}", response_model=ProductRead,)
def create_product(
    *,
    id: int
):
    return {}
