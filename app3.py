from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from qrcode import constants, QRCode
import tempfile

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def colorHEX2RGB(hex_color: str) -> tuple:
    """
    Converts a hexadecimal color to an RGB color.
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

@app.get("/")
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("form2.html", {"request": request}) # type: ignore

@app.post("/qrcode")
async def qrcode(
    text: str = Form(...),
    error_correction: str = Form(...),
    box_size: int = Form(10),
    border: int = Form(4),
    background_color: str = Form("#ffffff"),
    foreground_color: str = Form("#000000"),
    request: Request
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
        version = None,
        error_correction = error_correction_constant,
        box_size = box_size,
        border = border,
    )
    qr.add_data(text)
    qr.make(fit=True)
    fill = colorHEX2RGB(foreground_color)
    back_color = colorHEX2RGB(background_color)
    print(f"FG: {foreground_color}, BG: {background_color}")
    print(f"FG: {fill}, BG: {back_color}")
    img = qr.make_image(fill = fill, back_color = back_color)

    # with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
    #     img.save(temp_file)

    QRpng = img.save("QRpng.png")

    return templates.TemplateResponse("form3.html", {"request": request}) # type: ignore
