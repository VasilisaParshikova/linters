from pydantic import BaseModel


class BaseRecipe(BaseModel):
    title: str
    cooking_time: int


class RecipeInList(BaseRecipe):
    views: int

    class Config:
        orm_mode = True


class RecipeDetail(BaseRecipe):
    ingredients: str
    text: str

    class Config:
        orm_mode = True
