from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="Order Service")

VERSION = os.getenv("APP_VERSION", "dev")


class Order(BaseModel):
    customer: str
    amount: float


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": VERSION
    }


@app.get("/version")
def version():
    return {
        "version": VERSION
    }


@app.post("/orders")
def create_order(order: Order):
    return {
        "message": "Order accepted",
        "customer": order.customer,
        "amount": order.amount,
        "version": VERSION
    }