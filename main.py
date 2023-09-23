from fastapi import FastAPI
from pydantic import BaseModel


class AllocationData(BaseModel):
    s: list[int]
    p: list[int]
    l: list[int]


app = FastAPI()


@app.post("/generous")
async def generous(data: AllocationData):
    return {"message": "I am the generous algorithm"}


@app.post("/greedy")
async def greedy(data: AllocationData):
    return {"message": "I am the greedy algorithm"}


@app.post("/greedy-generous")
async def greedy_generous(data: AllocationData):
    return {"message": "I am the greedy-generous algorithm"}


@app.post("/the-other-one")
async def the_other_one(data: AllocationData):
    return {"message": "I am the the other algorithm"}
