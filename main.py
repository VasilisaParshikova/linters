from typing import List

from fastapi import FastAPI, Path
from sqlalchemy.future import select
from sqlalchemy import desc, func

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

@app.get('/recipes/', response_model=List[schemas.RecipeInList])
async def recipes() -> List[models.Recipe]:
    res = await session.execute(select(models.Recipe).order_by(desc(models.Recipe.views)))
    return res.scalars().all()

@app.get('/recipes/{id}', response_model=schemas.RecipeDetail)
async def recipes(
        id: int = Path(
        ...,
        title='Id of the recipe'
    )) -> models.Recipe:
    res = await session.execute(select(models.Recipe).where(models.Recipe.id == id))
    res = res.scalars().first()
    # if not res:
    #     return {"error": "No such recipe"}
    res.views += 1
    session.add(res)
    session.commit()
    return res
