from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from qrcode import constants, QRCode
import tempfile

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("form2.html", {"request": request})

@app.post("/qrcode")
async def qrcode(
    text: str = Form(...),
    version: int = Form(1),
    error_correction: str = Form("H"),
    box_size: int = Form(10),
    border: int = Form(4),
    background_color: str = Form("#ffffff"),
    foreground_color: str = Form("#000000")
):
    # Convert error_correction to the appropriate constant
    error_correction_mapping = {
        "H": constants.ERROR_CORRECT_H,
        "Q": constants.ERROR_CORRECT_Q,
        "M": constants.ERROR_CORRECT_M,
        "L": constants.ERROR_CORRECT_L,
    }
    error_correction_constant = error_correction_mapping.get(error_correction, constants.ERROR_CORRECT_H)

    qr = QRCode(
        version = version,
        error_correction = error_correction_constant,
        box_size = box_size,
        border = border,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill=foreground_color, back_color=background_color)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        img.save(temp_file, format="PNG")

    return FileResponse(temp_file.name, media_type="image/png")