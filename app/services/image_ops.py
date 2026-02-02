from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple
import PIL.ExifTags as ExifTags

def _open_image(image_bytes: bytes) -> Image.Image:
    return Image.open(BytesIO(image_bytes))

def compress_jpeg(image_bytes: bytes, quality: int = 75) -> bytes:
    img = _open_image(image_bytes).convert("RGB")
    out = BytesIO()
    img.save(out, format="JPEG", quality=int(quality), optimize=True)
    return out.getvalue()

def resize_image(image_bytes: bytes, max_width: int = 1200) -> bytes:
    img = _open_image(image_bytes)
    w, h = img.size
    if w > max_width:
        ratio = max_width / float(w)
        img = img.resize((max_width, int(h * ratio)))
    out = BytesIO()
    fmt = (img.format or "PNG").upper()
    if fmt not in ["PNG", "JPEG", "WEBP"]:
        fmt = "PNG"
    if fmt == "JPEG":
        img = img.convert("RGB")
    img.save(out, format=fmt)
    return out.getvalue()

def convert_image(image_bytes: bytes, fmt: str = "webp", quality: int = 85) -> Tuple[bytes, str]:
    img = _open_image(image_bytes)
    fmt = fmt.lower()
    if fmt not in ["jpg", "jpeg", "png", "webp"]:
        raise ValueError("format must be jpg/png/webp")

    out = BytesIO()
    if fmt in ["jpg", "jpeg"]:
        img = img.convert("RGB")
        img.save(out, format="JPEG", quality=int(quality), optimize=True)
        return out.getvalue(), "jpg"
    if fmt == "png":
        img = img.convert("RGBA")
        img.save(out, format="PNG")
        return out.getvalue(), "png"
    img = img.convert("RGBA")
    img.save(out, format="WEBP", quality=int(quality), method=6)
    return out.getvalue(), "webp"

def add_text_watermark(image_bytes: bytes, text: str="YourBrand", opacity: float=0.35, scale: float=0.06) -> bytes:
    base = _open_image(image_bytes).convert("RGBA")
    w, h = base.size

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = max(16, int(w * scale))
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    padding = int(font_size * 0.6)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = max(padding, w - tw - padding)
    y = max(padding, h - th - padding)

    alpha = max(0, min(255, int(255 * float(opacity))))
    draw.text((x, y), text, font=font, fill=(255, 255, 255, alpha))

    out = Image.alpha_composite(base, overlay)
    buf = BytesIO()
    out.save(buf, format="PNG")
    return buf.getvalue()

def extract_exif(image_bytes: bytes) -> dict:
    img = _open_image(image_bytes)
    exif = {}
    try:
        raw = img.getexif()
        if raw:
            for tag_id, value in raw.items():
                tag = ExifTags.TAGS.get(tag_id, str(tag_id))
                if isinstance(value, bytes):
                    value = value.decode(errors="ignore")
                exif[tag] = str(value)
    except Exception:
        pass
    return exif
