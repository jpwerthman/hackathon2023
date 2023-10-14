from fastapi import FastAPI
from models import MessageResponse, UserMessage
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a route using a decorator
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Define another route with a dynamic path parameter
@app.post("/message")
def read_item(message: UserMessage) -> dict:
    print(message.message)
    response_msg = MessageResponse(status=200, message=message.message)
    response_data = {'data': response_msg.dict()}  # Convert MessageResponse to a dictionary
    return response_data