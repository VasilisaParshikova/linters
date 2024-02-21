from sqlalchemy import Column, Integer, String

from database import Base


class Recipe(Base):
    __tablename__ = "recipe_table"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    ingredients = Column(String)
    text = Column(String)
    cooking_time = Column(Integer)
    views = Column(Integer)
