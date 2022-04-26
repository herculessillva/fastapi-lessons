from typing import Dict, List, Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None

items: List[Item] = []

@app.get("/examples")
async def get_example():
    return items

@app.post("/create_example")
async def post_example(item: Item):
    items.append(item)
    return item

@app.put("/update_example/{id}")
async def put_example(id: int, item: Item):
    items[id] = item
    return item

@app.delete("/delete_example")
async def delete_example(id: int):
    items.pop(id)
    return {"ok": True}