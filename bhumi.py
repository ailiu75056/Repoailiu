import json
import uvicorn # for local debugging
from actions import Action, Collection, ActionTypes
from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, HTMLReponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import uuid

CollectionsMockDB = {}

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/api/myactions", response_class=JSONResponse)
#returns actions infomation that a technician has performed
async def myactions(request: Request):
    return templates.TemplateResponse("myactions.html", {"request": request})

@app.get("api/myactions", response_class=JSONResponse)
#returns actions infomation that a technician has performed
async def myactions(request: Request):
    return templates.TemplateResponse("myactions.html", {"request": request})


@app.get("/api/{user_id}/purchases", response_class=JSONResponse)
#returns all the purchases made by a buyer
async def mypurchases(request: Request):
    return templates.TemplateResponse("mypurchases.html", {"request": request})

@app.get("/api/user/{user_id}", response_class=JSONResponse)
#returns information about a specific user
async def get_user(user_id: int, request: Request):
    return templates.TemplateResponse("user.html", {"request": request, "user_id": user_id})

@app.get("/api/purchase/{purchase_id}", response_class=JSONResponse)
# returns information about a specific purchase
async def get_purchase(purchase_id: int, request: Request):
    return templates.TemplateResponse("purchase.html", {"request": request, "purchase_id": purchase_id})


@app.get("/api/offset/{offset_id}", response_class=JSONResponse)
# returns information about a specific offset
async def get_offset(offset_id: int, request: Request):
    return templates.TemplateResponse("offset.html", {"request": request, "offset_id": offset_id})


@app.get("/api/action/{action_id}", response_class=JSONResponse)
    # returns information about a specific action
async def get_action(action_id: int, request: Request):
    return templates.TemplateResponse("action.html", {"request": request, "action_id": action_id})


@app.get("/api/document/{document_id}", response_class=JSONResponse)
# returns information about a specific document
async def get_document(document_id: int, request: Request):
    return templates.TemplateResponse("document.html", {"request": request, "document_id": document_id})

@app.post("/api/buyoffset/{amount}", response_class=JSONResponse)
# buy offset based on an amount
async def buy_offset(document_id: int, request: Request):
    return templates.TemplateResponse("offset.html", {"request": request, "document_id": document_id})

@app.post("/api/collection/add", response_class=JSONResponse)
# create a new purchase with refrigerant type, amount in KG, and amount paid
async def collection_add(refrigerantType: str, amountKG: float, request: Request, paymentAMT: float, paymentApiLink= ""):
    # perform logic to create a new purchase with the provided parameters
    
    id = "COL"+ str(uuid.uuid4())
    check = lambda x: x in CollectionsMockDB.keys() 
    if check(id) == True:
        id = "COL"+ str(uuid.uuid4())
        check(id)
    else:
        pass
    collection = Collection(id, refrigerantType = refrigerantType, amountKG = amountKG, paymentAMT =paymentAMT , paymentApiLink =paymentApiLink, createdDate = datetime.now(), actionType = ActionTypes.Collection)
    CollectionsMockDB[id] = collection
    return templates.TemplateResponse("purchase.html", {"request": request, "refrigerantType": refrigerantType, "amountKG": amountKG, "amountPaid": paymentAMT, "paymentApiLink": paymentApiLink})



