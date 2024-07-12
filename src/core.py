from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
app = FastAPI(title="website")


@app.get('/',response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("chats/chat.html", {"request":request})

