from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Music"
)
users3 = []
users = [
    {"id": 1, "role": "Admin", "Name": "Senya"},
    {"id": 2, "role": "Listner", "Name": "Sergey"},
    {"id": 3, "role": "Compositor", "Name": "Nemo"},
]


music_add = [
    {"id": 1, "user_id": 1, "Name": "Tears don't fall"},
    {"id": 2, "user_id": 1, "Name": "Rap God"},
    {"id": 3, "user_id": 1, "Name": "Your betrayed"},
]


class User(BaseModel):
    id: int
    role: str
    Name: str


@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in users if user.get("id") == user_id]


@app.get("/Janrs")
def get_janrs(kol_vo_janrs: int = 1, offset: int = 0):
    return music_add[offset:][:kol_vo_janrs]


@app.post("/users")
def post_user(user: str):
    users3.append(user)
    return users3


@app.post("/users/{user_id}")
def change_user_role(user_id: int, new_role: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, users))[0]
    current_user["role"] = new_role
    return{"status": 200, "data": current_user}


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post("/trades")
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}


