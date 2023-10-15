from fastapi import FastAPI
from models import MessageResponse, UserMessage, AuthDetailsRequest
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ourAI import Bot
from auth import AuthHandler

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://localhost:8000"
]

ourBot = Bot()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_handler = AuthHandler()
users = []

# Define a route using a decorator
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Define another route with a dynamic path parameter
@app.post("/message")
def read_item(message: UserMessage, username=Depends(auth_handler.authWrapper)):
    # Call the function that runs the conversation
    response = ourBot.run_conversation(message.message)
    print(response)
    # extractedMessage = response.choices[0].message.content
    # print(response.choices.message.content)
    response_msg = MessageResponse(status=200, botResponse=response)
    response_data = JSONResponse(status_code=200, content=response_msg.dict())  # Convert MessageResponse to a dictionary
    return response_data


@app.post('/register', status_code=201)
def register(auth_details: AuthDetailsRequest):
    # Instead of checking it from the list, I would check against the database
    print(auth_details)
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    # Get the hashed password for the user registering
    hashed_pass = auth_handler.getPasswordHash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_pass
    })
    return {'status': "ok"}

@app.post("/login")
async def login(auth_details: AuthDetailsRequest, response: Response):
    # Look for user in the 'database' users = []
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break
    # user not found
    if (user is None) or (not auth_handler.verifyPassword(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token, expire = auth_handler.createAccessToken(user['username'])
    response = JSONResponse(content={'token': token})
    response.set_cookie(key="token",
                        value=token,
                        httponly=True,
                        secure=True,
                        expires=expire.strftime("%a, %d %b %Y %H:%M:%S GMT"))
    return response
