from fastapi import FastAPI
from models import MessageResponse, UserMessage, AuthDetailsRequest
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ourAI import Bot
from auth import AuthHandler
import requests

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
customerId = 7006556796

# Define a route using a decorator
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Define another route with a dynamic path parameter
@app.post("/message")
def read_item(message: UserMessage):
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

@app.post("/getTransactions")
async def getTransactions(request: Request):
    url = 'https://api.finicity.com/aggregation/v3/customers/7006574789/transactions?fromDate=1000000000&toDate=1665309262'

    # Headers
    headers = {
        'Finicity-App-Key': 'd4f1adef749e28e08b7303189c08f24d',
        'Accept': 'application/json',
        'Finicity-App-Token': 'b65QjYdAW7paBbT9P1gk',
        'Cookie': 'incap_ses_113_2596171=9Nj2JG7ac0nQcRkr8HWRATt6K2UAAAAACTkdlOe5NJcFupIkn6q4wQ==; nlbi_2596171=laaqSedd/xU296k5pbFNgwAAAAAUsUNiycBcDdOAEOgld96O; visid_incap_2596171=DrcJ3851SKWp6sRIbBPnoZkuK2UAAAAAQUIPAAAAAAD9ok+1RbF+HXYtc6pdOaNV'
    }

    # Making the GET request
    response = requests.get(url, headers=headers)
    bot = Bot()
    # Check the response
    allTrans = response.json().get('transactions')
    allTrans = ourBot.JSONtoCSV(allTrans)
    ourBot.set_transaction_info(allTrans)
    print("Get transaction", allTrans)
    

