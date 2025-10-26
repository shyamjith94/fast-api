from app.api.schema import Base, CommonBase

class CategoryBase(Base):
    name:str
    description:str


class CategoryCreate(CategoryBase):
    pass



class CategoryRead(CategoryBase, CommonBase):
    class Config:
        orm_mode=True