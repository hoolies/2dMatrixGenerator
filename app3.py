from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from qrcode import constants, QRCode
from tempfile import NamedTemporaryFile


# Create the FastAPI app
app = FastAPI()

# Set the Jinja2 templates directory
templates = Jinja2Templates(directory="templates")


def colorHEX2RGB(hex_color: str) -> tuple:
    """
    Converts a hexadecimal color to an RGB color.
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


@app.get("/")
async def root(request: Request) -> HTMLResponse:
    """Serves the home page."""
    return templates.TemplateResponse("form3.html", {"request": request}) # type: ignore

@app.post("/qrcode")
async def qrcode(
    text: str = Form(...),
    error_correction: str = Form(...),
    box_size: int = Form(10),
    border: int = Form(4),
    background_color: str = Form("#ffffff"),
    foreground_color: str = Form("#000000"),
):
    """Generates a QR code based on the form data."""
    
    # Convert error_correction to the appropriate constant
    error_correction_mapping = {
        "H": constants.ERROR_CORRECT_H,
        "Q": constants.ERROR_CORRECT_Q,
        "M": constants.ERROR_CORRECT_M,
        "L": constants.ERROR_CORRECT_L,
    }
    # Set the error correction constant
    error_correction_constant = error_correction_mapping.get(error_correction, constants.ERROR_CORRECT_H)

    # Generate QR codeq
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
    img = qr.make_image(fill = fill, back_color = back_color)

    # Save the QR code to a temporary file
    with NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        img.save(temp_file.name)
        tempqr = temp_file.name

    # Return the QR code image as a downloadable file    
    return FileResponse(tempqr, headers={"Content-Disposition": "attachment; filename=QRcode.png"})