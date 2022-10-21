from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .Routes import Payments

app = FastAPI()

app.include_router(Payments.root)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("/")
def root():
    return {"Condition":"Good"}