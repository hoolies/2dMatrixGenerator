from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from qrcode import constants, QRCode
import tempfile

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/qrcode")
async def qrcode(text: str = Form(...)):  # Use "text" to match the input field name
    qr = QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image()

    # Create a temporary file to save the QR code image
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        img.save(temp_file, format="PNG")

    # Return the image file using FileResponse
    return FileResponse(temp_file.name, media_type="image/png")
