from typing import List, Sequence, Union

from fastapi import FastAPI, Path
from sqlalchemy import desc, func
from sqlalchemy.future import select

import models
import schemas
from database import engine, session

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.get("/recipes/", response_model=Sequence[schemas.RecipeInList])
async def recipes() -> Sequence[models.Recipe]:
    res = await session.execute(
        select(models.Recipe).order_by(desc(models.Recipe.views))
    )
    return res.scalars().all()


@app.get("/recipes/{id}", response_model=schemas.RecipeDetail)
async def recipes_id(
    id: int = Path(..., title="Id of the recipe")
) -> Union[models.Recipe, None]:
    res = await session.execute(select(models.Recipe).where(models.Recipe.id == id))
    res_1 = res.scalars().first()
    # if not res:
    #     return {"error": "No such recipe"}
    if res_1:
        res_1.views = res_1.views + 1
        session.add(res)
        session.commit()
    return res_1
