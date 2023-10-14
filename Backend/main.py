from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/bot")
def read_item():
    return {"botResponse": "This is a Test!"}
