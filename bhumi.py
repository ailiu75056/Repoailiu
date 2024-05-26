import json
import uvicorn # for local debugging

from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get("api/myactions", response_class=HTMLResponse)
#returns actions infomation that a technician has performed
async def myactions(request: Request):
    return templates.TemplateResponse("myactions.html", {"request": request})


@app.get("/api/purchases", response_class=HTMLResponse)
#returns all the purchases made by a buyer
async def mypurchases(request: Request):
    return templates.TemplateResponse("mypurchases.html", {"request": request})

@app.get("/api/user/{user_id}", response_class=HTMLResponse)
#returns information about a specific user
async def get_user(user_id: int, request: Request):
    return templates.TemplateResponse("user.html", {"request": request, "user_id": user_id})

@app.get("/api/purchase/{purchase_id}", response_class=HTMLResponse)
# returns information about a specific purchase
async def get_purchase(purchase_id: int, request: Request):
    return templates.TemplateResponse("purchase.html", {"request": request, "purchase_id": purchase_id})


@app.get("/api/offset/{offset_id}", response_class=HTMLResponse)
# returns information about a specific offset
async def get_offset(offset_id: int, request: Request):
    return templates.TemplateResponse("offset.html", {"request": request, "offset_id": offset_id})


@app.get("/api/action/{action_id}", response_class=HTMLResponse)
    # returns information about a specific action
async def get_action(action_id: int, request: Request):
    return templates.TemplateResponse("action.html", {"request": request, "action_id": action_id})


@app.get("/api/document/{document_id}", response_class=HTMLResponse)
# returns information about a specific document
async def get_document(document_id: int, request: Request):
    return templates.TemplateResponse("document.html", {"request": request, "document_id": document_id})

@app.get("/api/buyoffset/{amount}", response_class=HTMLResponse)
# buy offset based on an amount
async def get_document(document_id: int, request: Request):
    return templates.TemplateResponse("document.html", {"request": request, "document_id": document_id})


