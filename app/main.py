import os
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from unoserver.client import UnoClient

app = FastAPI()
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

UNOSERVER_HOST = os.getenv("UNOSERVER_HOST", "localhost")
UNOSERVER_PORT = os.getenv("UNOSERVER_PORT", "2003")
CONVERTED_DIR = Path("/tmp/converted")
CONVERTED_DIR.mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/convert", response_class=HTMLResponse)
async def convert(request: Request, file: UploadFile):
    indata = await file.read()
    stem = Path(file.filename).stem if file.filename else "output"
    out_filename = f"{stem}_{uuid.uuid4().hex[:8]}.pdf"
    out_path = CONVERTED_DIR / out_filename

    client = UnoClient(server=UNOSERVER_HOST, port=UNOSERVER_PORT)
    result = client.convert(indata=indata, convert_to="pdf")

    out_path.write_bytes(result)

    return templates.TemplateResponse(
        request,
        "result.html",
        {"filename": out_filename, "original": file.filename},
    )


@app.get("/download/{filename}")
async def download(filename: str):
    file_path = CONVERTED_DIR / filename
    if not file_path.exists():
        return HTMLResponse("<p>ファイルが見つかりません。</p>", status_code=404)
    return FileResponse(file_path, filename=filename, media_type="application/pdf")
