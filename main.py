from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Workshop API")

class Item(BaseModel):
    id: Optional[int] = None  # ← просто None, без Field(exclude=True)
    name: str
    description: Optional[str] = None
    price: float

class User(BaseModel):
    id: Optional[int] = None  # ← просто None
    username: str
    email: str

items_db = []
users_db = []
next_item_id = 1
next_user_id = 1

@app.get("/")
async def root():
    return {"message": "Welcome to Workshop API"}

@app.get("/items", response_model=List[Item])
async def get_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = next((i for i in items_db if i.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: Item):
    global next_item_id
    new_item = Item(id=next_item_id, **item.model_dump(exclude={'id'}))
    items_db.append(new_item)
    next_item_id += 1
    return new_item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    db_item = next((i for i in items_db if i.id == item_id), None)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.description = item.description
    db_item.price = item.price
    return db_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    global items_db
    item = next((i for i in items_db if i.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db = [i for i in items_db if i.id != item_id]
    return {"message": "Item deleted"}

@app.get("/users", response_model=List[User])
async def get_users():
    return users_db

@app.post("/users", response_model=User, status_code=201)
async def create_user(user: User):
    global next_user_id
    new_user = User(id=next_user_id, **user.model_dump(exclude={'id'}))
    users_db.append(new_user)
    next_user_id += 1
    return new_user