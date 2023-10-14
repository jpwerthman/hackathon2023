from fastapi import FastAPI

app = FastAPI()

# Define a route using a decorator
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Define another route with a dynamic path parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}
