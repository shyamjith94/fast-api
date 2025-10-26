from app.api.models import ModelBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, CheckConstraint, ForeignKey, String, Float, Integer
from app.api.models import Category

class Product(ModelBase):
    __tablename__ ="products"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False, )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    category_id:Mapped[UUID] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False,)
    category:Mapped["Category"] = relationship("Category",)

    __table_args__ = (
        CheckConstraint("price>=0", name="price should greater then zero"),
        CheckConstraint("quantity>=0", name="quantity should greater then zero")
    )

    def __str__(self):
        return self.name
