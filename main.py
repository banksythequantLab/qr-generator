from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import Response, FileResponse
from PIL import Image
import qrcode
import io

app = FastAPI()


@app.get("/")
async def read_index():
    return FileResponse('index.html')



def generate_qr(url: str, box_size: int = 10, border: int = 4) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # high for logo/overlay robustness
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    return img


def overlay_qr_on_image(
    base_img: Image.Image,
    qr_img: Image.Image,
    position: str = "bottom_right",
    margin: int = 32,
    qr_frac_of_width: float = 0.2,
) -> Image.Image:
    base = base_img.convert("RGBA")
    w, h = base.size

    # Resize QR relative to base width
    target_qr_width = int(w * qr_frac_of_width)
    ratio = target_qr_width / qr_img.width
    target_qr_height = int(qr_img.height * ratio)
    qr_resized = qr_img.resize((target_qr_width, target_qr_height), Image.LANCZOS)

    bw, bh = base.size
    qw, qh = qr_resized.size

    if position == "top_left":
        x, y = margin, margin
    elif position == "top_right":
        x, y = bw - qw - margin, margin
    elif position == "bottom_left":
        x, y = margin, bh - qh - margin
    else:  # bottom_right default
        x, y = bw - qw - margin, bh - qh - margin

    base.paste(qr_resized, (x, y), qr_resized)
    return base


def make_qr_with_logo(
    url: str,
    logo_img: Image.Image,
    qr_size: int = 800,
    logo_frac: float = 0.25,
) -> Image.Image:
    qr = generate_qr(url, box_size=10, border=4)
    qr = qr.resize((qr_size, qr_size), Image.LANCZOS)

    logo = logo_img.convert("RGBA")
    lw = int(qr_size * logo_frac)
    ratio = lw / logo.width
    lh = int(logo.height * ratio)
    logo = logo.resize((lw, lh), Image.LANCZOS)

    # center logo
    x = (qr_size - lw) // 2
    y = (qr_size - lh) // 2

    qr.paste(logo, (x, y), logo)
    return qr


@app.post("/qr-with-image")
async def qr_with_image(
    image: UploadFile = File(...),
    url: str = Form(...),
    mode: str = Form("overlay"),
    position: str = Form("bottom_right"),
    qr_size: float = Form(0.2),
    margin: int = Form(32),
    output_format: str = Form("png"),
):
    # Load base image
    img_bytes = await image.read()
    base_img = Image.open(io.BytesIO(img_bytes))

    if mode == "logo":
        # image is used as logo in middle of QR
        result = make_qr_with_logo(url, base_img)
    else:
        # generate QR, then overlay on top of base image
        qr_img = generate_qr(url)
        result = overlay_qr_on_image(
            base_img,
            qr_img,
            position=position,
            margin=margin,
            qr_frac_of_width=qr_size,
        )

    buf = io.BytesIO()
    fmt = "PNG" if output_format.lower() == "png" else "JPEG"
    result.save(buf, format=fmt)
    buf.seek(0)

    mime = "image/png" if fmt == "PNG" else "image/jpeg"
    return Response(content=buf.getvalue(), media_type=mime)
