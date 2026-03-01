import os
from pathlib import Path

from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from unoserver.client import UnoClient

app = FastAPI()
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

UNOSERVER_HOST = os.getenv("UNOSERVER_HOST", "localhost")
UNOSERVER_PORT = os.getenv("UNOSERVER_PORT", "2003")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/convert")
async def convert(file: UploadFile):
    indata = await file.read()
    stem = Path(file.filename).stem if file.filename else "output"
    out_filename = f"{stem}.pdf"

    client = UnoClient(server=UNOSERVER_HOST, port=UNOSERVER_PORT)
    result = client.convert(indata=indata, convert_to="pdf")

    return Response(
        content=result,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{out_filename}"'},
    )
