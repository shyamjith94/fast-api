from sqlalchemy import String
from app.api.models import ModelBase
from sqlalchemy.orm import Mapped, mapped_column


class Category(ModelBase):

    __tablename__ = "categories"

    name:Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description:Mapped[str] = mapped_column(String(100), nullable=True)


    def __str__(self):
        return self.name