from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from app.api.depends.database.session import Database
from app.api.models import Category
from app.api.schema.categories.category_schema import CategoryCreate, CategoryRead

category_router = APIRouter(prefix="/categories")

db_class = Database()


@category_router.get("/", response_model=List[CategoryRead])
def get_category(*, db: Database = Depends(db_class.get_db)):
    try:
        categories = db.query(Category).all()
        return categories
    except Exception as e:
        raise HTTPException(status_code=500,)


# @category_router.get("/{id}", response_model=CategoryRead)
# def get_categories(*, id: int, db: Database= Database(db_class.get_db)):
#     try:
#         categories = db.query(Category).all()
#         return categories
#     except Exception as e:
#         raise HTTPException(status_code=500,)


@category_router.post("/", response_model=CategoryRead)
def create_category(*, cate_in: CategoryCreate, db: Database = Depends(db_class.get_db)):
    try:
        category = Category(**cate_in.model_dump())
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

# @category_router.patch("/{id}")
# def get_category(*, id: int, db: Database= Database(db_class.get_db)):
#     return {}

# @category_router.put("/{id}")
# def get_category(*, id: int, db: Database= Database(db_class.get_db)):
#     return {}


# @category_router.delete("/{id}")
# def get_category(*, id: int, db: Database= Database(db_class.get_db)):
#     return {}
