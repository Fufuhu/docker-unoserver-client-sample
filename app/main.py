import os
from pathlib import Path

from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
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
    # アップロードされたファイルの内容をバイト列として読み込む
    indata = await file.read()

    # 元のファイル名から拡張子を除いた部分を取得し、ダウンロード用のPDFファイル名を生成する
    stem = Path(file.filename).stem if file.filename else "output"
    out_filename = f"{stem}.pdf"

    # unoserverに接続するクライアントを作成する（XMLRPC経由で通信）
    client = UnoClient(server=UNOSERVER_HOST, port=UNOSERVER_PORT)

    # ファイルのバイト列をunoserverに送信し、PDF形式に変換する
    # 変換結果はPDFのバイト列として返される
    result = client.convert(indata=indata, convert_to="pdf")

    # 変換されたPDFをレスポンスとして返す
    # Content-Dispositionヘッダーにより、ブラウザがファイルを直接ダウンロードする
    return Response(
        content=result,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{out_filename}"'},
    )
