from typing import List, Optional
from fastapi.exceptions import HTTPException
from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from numpy import size

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
    id: Optional[int]
    role: Optional[str]
    Name: Optional[str]


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=List[User])
def get_user(user_id: int = 1):
    if 0 >= user_id or user_id > size(users):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong id")

    return [user for user in users if user.get("id") == user_id]


@app.get("/Music_list", status_code=status.HTTP_200_OK)
def get_song(music_list_id: int = 1, offset: int = 0):
    if 0 >= music_list_id or music_list_id > size(music_add):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong id")

    return music_add[offset:][:music_list_id]


@app.post("/users", status_code=status.HTTP_200_OK)
def post_user(user: str):
    users3.append(user)
    return users3


@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
def change_user_role(user_id: int = 1, new_role: str = "Null"):
    if 0 >= user_id or user_id > size(users):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong id")

    current_user = list(filter(lambda user: user.get("id") == user_id, users))[0]
    current_user["role"] = new_role
    return{"status": 200, "data": current_user}


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
]


class Trade(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    currency: Optional[str] = Field(max_length=5)
    side: Optional[str]
    price: Optional[float] = Field(ge=0)
    amount: Optional[float]


@app.post("/trades", status_code=status.HTTP_200_OK)
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}
